"""
Grad-CAM (Gradient-weighted Class Activation Mapping).

Reference: Selvaraju et al., 2017 — https://arxiv.org/abs/1610.02391

Given a trained model and an input image, produces a heatmap highlighting
the regions the model attended to when making its prediction.
"""
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image

import config


def _find_last_conv_layer(model):
    """Walk the model backwards and return the last Conv2D layer's name.
    Handles wrapped Keras Application backbones (Sequential / Functional)."""
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
        # If layer is itself a Model (e.g. MobileNetV2 backbone), recurse.
        if hasattr(layer, "layers"):
            for inner in reversed(layer.layers):
                if isinstance(inner, tf.keras.layers.Conv2D):
                    # Return the *sub-model* layer name; caller handles that.
                    return layer.name
    raise ValueError("No Conv2D layer found in model.")


def make_gradcam_heatmap(img_array, model, pred_index=None):
    """
    Produce a Grad-CAM heatmap as a 2D numpy array in [0, 1].

    img_array : preprocessed batch, shape (1, H, W, 3)
    model     : trained Keras model
    pred_index: class index to explain (default: top prediction)
    """
    last_conv_layer_name = _find_last_conv_layer(model)
    last_conv_layer = model.get_layer(last_conv_layer_name)

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[last_conv_layer.output, model.output],
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()


def overlay_heatmap(original_image_path: str, heatmap: np.ndarray,
                    output_path: str, alpha: float = 0.4):
    """Save a JPG that overlays the Grad-CAM heatmap on the original image."""
    img = cv2.imread(original_image_path)
    img = cv2.resize(img, (config.IMG_SIZE, config.IMG_SIZE))

    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.resize(heatmap, (config.IMG_SIZE, config.IMG_SIZE))
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(img, 1 - alpha, heatmap_color, alpha, 0)
    cv2.imwrite(output_path, overlay)
    return output_path
