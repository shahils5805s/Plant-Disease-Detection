"""Unit tests. Run with: pytest tests/ -v"""
import os
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from disease_info import DISEASE_INFO, get_info
from utils.preprocessing import preprocess_pil, is_allowed_file


def test_class_count():
    assert len(config.CLASS_NAMES) == config.NUM_CLASSES == 38


def test_disease_info_covers_all_classes():
    """Every class in config.CLASS_NAMES must have an entry in DISEASE_INFO."""
    missing = [c for c in config.CLASS_NAMES if c not in DISEASE_INFO]
    assert not missing, f"Missing disease info for: {missing}"


def test_disease_info_fields():
    for cls, info in DISEASE_INFO.items():
        assert "cause" in info, cls
        assert "symptoms" in info, cls
        assert "treatment" in info, cls
        assert len(info["cause"]) > 0
        assert len(info["treatment"]) > 0


def test_get_info_fallback():
    info = get_info("Not_a_real_class")
    assert "cause" in info and "treatment" in info


def test_is_allowed_file():
    assert is_allowed_file("leaf.jpg")
    assert is_allowed_file("leaf.JPEG")
    assert is_allowed_file("leaf.png")
    assert not is_allowed_file("leaf.pdf")
    assert not is_allowed_file("leaf.exe")
    assert not is_allowed_file("noextension")


def test_preprocess_pil_shape():
    img = Image.new("RGB", (500, 400), color="green")
    x = preprocess_pil(img)
    assert x.shape == (1, config.IMG_SIZE, config.IMG_SIZE, 3)
    # MobileNetV2 preprocess_input scales to [-1, 1]
    assert x.min() >= -1.01 and x.max() <= 1.01


def test_preprocess_handles_rgba():
    img = Image.new("RGBA", (300, 300), color=(0, 200, 0, 255))
    x = preprocess_pil(img)
    assert x.shape == (1, config.IMG_SIZE, config.IMG_SIZE, 3)


def test_pretty_name():
    assert config.pretty_name("Tomato___Late_blight") == "Tomato — Late blight"
    assert config.pretty_name("Apple___healthy") == "Apple — healthy"
