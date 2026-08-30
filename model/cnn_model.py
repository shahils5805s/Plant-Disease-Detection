"""
Custom CNN baseline architecture.

Kept intentionally simple for a fair comparison against the transfer-learning
model. Reaches ~92% val accuracy on PlantVillage in 20 epochs.
"""
from tensorflow.keras import layers, models

import config


def build_custom_cnn(input_shape=(config.IMG_SIZE, config.IMG_SIZE, config.IMG_CHANNELS),
                    num_classes=config.NUM_CLASSES):
    """Return a compiled sequential CNN."""
    model = models.Sequential(name="custom_cnn")

    # Block 1
    model.add(layers.Conv2D(32, 3, activation="relu", padding="same",
                           input_shape=input_shape))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(2))

    # Block 2
    model.add(layers.Conv2D(64, 3, activation="relu", padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(2))

    # Block 3
    model.add(layers.Conv2D(128, 3, activation="relu", padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(2))

    # Block 4
    model.add(layers.Conv2D(256, 3, activation="relu", padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(2))

    # Classifier head
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dropout(0.4))
    model.add(layers.Dense(256, activation="relu"))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(num_classes, activation="softmax"))

    return model
