"""
Train a plant disease classifier on the PlantVillage dataset.

Usage:
  python train.py                            # default: MobileNetV2, 20 epochs
  python train.py --model cnn --epochs 30
  python train.py --model transfer --epochs 25 --batch-size 64

Prerequisite: data directory must exist at config.DATA_DIR with one
sub-folder per class. Run `python download_dataset.py` first.
"""
import argparse
import os
from datetime import datetime

import tensorflow as tf
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                         ReduceLROnPlateau, TensorBoard)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import config
from model import (build_custom_cnn, build_transfer_model,
                   unfreeze_top_layers)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=["cnn", "transfer"], default="transfer")
    p.add_argument("--epochs", type=int, default=config.EPOCHS)
    p.add_argument("--batch-size", type=int, default=config.BATCH_SIZE)
    p.add_argument("--data-dir", default=config.DATA_DIR)
    p.add_argument("--no-fine-tune", action="store_true",
                   help="Skip phase 2 (fine-tuning) for transfer model")
    return p.parse_args()


def build_data_generators(data_dir, batch_size):
    """Standard PlantVillage augmentation."""
    train_gen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
        rotation_range=30,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=False,
        fill_mode="nearest",
        validation_split=config.VALIDATION_SPLIT,
    )

    train = train_gen.flow_from_directory(
        data_dir,
        target_size=(config.IMG_SIZE, config.IMG_SIZE),
        batch_size=batch_size,
        class_mode="categorical",
        subset="training",
        shuffle=True,
        seed=42,
    )
    val = train_gen.flow_from_directory(
        data_dir,
        target_size=(config.IMG_SIZE, config.IMG_SIZE),
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation",
        shuffle=False,
        seed=42,
    )
    return train, val


def make_callbacks(tag: str):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    logdir = os.path.join(config.LOG_DIR, f"{tag}-{ts}")
    return [
        ModelCheckpoint(config.MODEL_PATH, save_best_only=True,
                        monitor="val_accuracy", mode="max", verbose=1),
        EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3,
                          min_lr=1e-7, verbose=1),
        TensorBoard(log_dir=logdir),
    ]


def train_transfer(args):
    train, val = build_data_generators(args.data_dir, args.batch_size)
    model, base = build_transfer_model(trainable_backbone=False)

    # ---- Phase 1: frozen backbone ----
    print("\n=== PHASE 1: Training classifier head (backbone frozen) ===")
    model.compile(optimizer=Adam(config.LEARNING_RATE),
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    model.summary()
    phase1_epochs = min(5, args.epochs)
    model.fit(train, epochs=phase1_epochs, validation_data=val,
              callbacks=make_callbacks("phase1"), verbose=1)

    if args.no_fine_tune or args.epochs <= phase1_epochs:
        return model

    # ---- Phase 2: unfreeze top layers ----
    print("\n=== PHASE 2: Fine-tuning top 30 layers of backbone ===")
    unfreeze_top_layers(base, n=30)
    model.compile(optimizer=Adam(config.FINE_TUNE_LR),
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    remaining = args.epochs - phase1_epochs
    model.fit(train, epochs=remaining, validation_data=val,
              callbacks=make_callbacks("phase2"), verbose=1)
    return model


def train_custom_cnn(args):
    train, val = build_data_generators(args.data_dir, args.batch_size)
    model = build_custom_cnn()
    model.compile(optimizer=Adam(config.LEARNING_RATE),
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    model.summary()
    model.fit(train, epochs=args.epochs, validation_data=val,
              callbacks=make_callbacks("cnn"), verbose=1)
    return model


def main():
    args = parse_args()

    if not os.path.isdir(args.data_dir):
        raise SystemExit(
            f"Data directory not found: {args.data_dir}\n"
            "Run `python download_dataset.py` first, or point --data-dir "
            "at a folder with one sub-folder per class."
        )

    print(f"TensorFlow: {tf.__version__}")
    print(f"GPUs available: {tf.config.list_physical_devices('GPU')}")

    if args.model == "transfer":
        model = train_transfer(args)
    else:
        model = train_custom_cnn(args)

    model.save(config.MODEL_PATH)
    print(f"\n[✓] Model saved to {config.MODEL_PATH}")


if __name__ == "__main__":
    main()
