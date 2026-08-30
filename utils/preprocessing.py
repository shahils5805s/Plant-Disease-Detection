"""Image preprocessing helpers used by both training and inference."""
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

import config


def load_and_preprocess(image_path: str) -> np.ndarray:
    """
    Load an image from disk, resize, and preprocess for MobileNetV2.
    Returns a batch of shape (1, IMG_SIZE, IMG_SIZE, 3).
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize((config.IMG_SIZE, config.IMG_SIZE))
    arr = np.array(img, dtype=np.float32)
    arr = preprocess_input(arr)  # scales to [-1, 1] as MobileNetV2 expects
    return np.expand_dims(arr, axis=0)


def preprocess_pil(img: Image.Image) -> np.ndarray:
    """Same as above but taking a PIL image directly (used by the web app)."""
    img = img.convert("RGB").resize((config.IMG_SIZE, config.IMG_SIZE))
    arr = np.array(img, dtype=np.float32)
    arr = preprocess_input(arr)
    return np.expand_dims(arr, axis=0)


def is_allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )
