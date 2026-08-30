"""
Command-line prediction utility.

Usage:
  python predict.py --image path/to/leaf.jpg
  python predict.py --image path/to/leaf.jpg --gradcam out.jpg
"""
import argparse
import os
import sys

import numpy as np
import tensorflow as tf

import config
from disease_info import get_info
from utils.preprocessing import load_and_preprocess
from utils.grad_cam import make_gradcam_heatmap, overlay_heatmap


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--image", required=True, help="Path to leaf image")
    p.add_argument("--model", default=config.MODEL_PATH,
                   help="Path to trained .h5 model")
    p.add_argument("--gradcam", default=None,
                   help="If set, save Grad-CAM overlay to this path")
    p.add_argument("--top-k", type=int, default=3)
    return p.parse_args()


def predict(image_path, model, top_k=3):
    x = load_and_preprocess(image_path)
    probs = model.predict(x, verbose=0)[0]
    top_idx = np.argsort(probs)[-top_k:][::-1]
    return [
        {
            "class": config.CLASS_NAMES[i],
            "confidence": float(probs[i]),
        }
        for i in top_idx
    ], x, int(top_idx[0])


def main():
    args = parse_args()

    if not os.path.exists(args.image):
        sys.exit(f"Image not found: {args.image}")
    if not os.path.exists(args.model):
        sys.exit(
            f"Model not found: {args.model}\n"
            "Train one first: `python train.py`"
        )

    model = tf.keras.models.load_model(args.model)
    predictions, x, top_idx = predict(args.image, model, args.top_k)

    top = predictions[0]
    info = get_info(top["class"])

    print("\n=== Prediction ===")
    print(f"Top class : {config.pretty_name(top['class'])}")
    print(f"Confidence: {top['confidence']*100:.1f}%")
    print(f"\nTop-{args.top_k}:")
    for p in predictions:
        print(f"  {p['confidence']*100:5.1f}%  {config.pretty_name(p['class'])}")

    print("\n=== Disease Info ===")
    print(f"Cause    : {info['cause']}")
    print(f"Symptoms : {info['symptoms']}")
    print(f"Treatment: {info['treatment']}")

    if args.gradcam:
        heatmap = make_gradcam_heatmap(x, model, pred_index=top_idx)
        overlay_heatmap(args.image, heatmap, args.gradcam)
        print(f"\n[✓] Grad-CAM overlay saved to {args.gradcam}")


if __name__ == "__main__":
    main()
