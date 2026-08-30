"""
Flask web app + REST API for the Plant Disease Detection system.

Routes:
  GET  /                 upload form
  POST /predict          web form submission → result page
  GET  /about            project info
  POST /api/predict      JSON API (multipart/form-data with 'image' field)
  GET  /api/classes      list of all supported disease classes
  GET  /health           health check

Runs in DEMO MODE if no trained model file exists — useful for
previewing the UI before you've trained anything.
"""
import os
import uuid
import logging
from pathlib import Path

import numpy as np
from flask import (Flask, render_template, request, jsonify, url_for,
                   redirect, flash, abort)
from PIL import Image
from werkzeug.utils import secure_filename

import config
from disease_info import get_info
from utils.preprocessing import preprocess_pil, is_allowed_file

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("plant-disease")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config.UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = config.MAX_UPLOAD_SIZE_MB * 1024 * 1024
app.secret_key = os.environ.get("FLASK_SECRET", "change-me-in-production")

# ---------- Load model once at startup ----------
MODEL = None
DEMO_MODE = False


def load_model_if_available():
    global MODEL, DEMO_MODE
    if os.path.exists(config.MODEL_PATH):
        try:
            import tensorflow as tf
            log.info(f"Loading model from {config.MODEL_PATH}")
            MODEL = tf.keras.models.load_model(config.MODEL_PATH)
            log.info("Model loaded ✓")
        except Exception as e:
            log.exception("Model load failed, falling back to demo mode")
            DEMO_MODE = True
    else:
        log.warning("No trained model found — running in DEMO MODE. "
                    "Train with `python train.py` to enable real predictions.")
        DEMO_MODE = True


load_model_if_available()


# ---------- Prediction helper ----------
def run_prediction(image_path: str, top_k: int = 3):
    """Return (top_k predictions list, top class index)."""
    if DEMO_MODE:
        # Deterministic pseudo-random demo output based on filename hash
        # so recruiters can preview the UI without training.
        rng = np.random.default_rng(abs(hash(image_path)) % (2**32))
        probs = rng.dirichlet(np.ones(config.NUM_CLASSES) * 0.5)
        # Bias one class up so the output looks plausible
        boost_idx = rng.integers(0, config.NUM_CLASSES)
        probs[boost_idx] += 0.85
        probs = probs / probs.sum()
    else:
        img = Image.open(image_path)
        x = preprocess_pil(img)
        probs = MODEL.predict(x, verbose=0)[0]

    top_idx = np.argsort(probs)[-top_k:][::-1]
    predictions = [
        {
            "class": config.CLASS_NAMES[i],
            "pretty": config.pretty_name(config.CLASS_NAMES[i]),
            "confidence": float(probs[i]),
        }
        for i in top_idx
    ]
    return predictions, int(top_idx[0])


def try_gradcam(image_path: str, top_idx: int):
    """Generate a Grad-CAM overlay if we have a real model. Returns URL or None."""
    if DEMO_MODE or MODEL is None:
        return None
    try:
        from utils.grad_cam import make_gradcam_heatmap, overlay_heatmap
        img = Image.open(image_path)
        x = preprocess_pil(img)
        heatmap = make_gradcam_heatmap(x, MODEL, pred_index=top_idx)
        out_path = image_path.rsplit(".", 1)[0] + "_gradcam.jpg"
        overlay_heatmap(image_path, heatmap, out_path)
        return url_for("static",
                       filename=f"uploads/{os.path.basename(out_path)}")
    except Exception:
        log.exception("Grad-CAM failed")
        return None


# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html", demo_mode=DEMO_MODE)


@app.route("/predict", methods=["POST"])
def predict_web():
    if "image" not in request.files:
        flash("No file selected.", "error")
        return redirect(url_for("index"))

    file = request.files["image"]
    if file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("index"))

    if not is_allowed_file(file.filename):
        flash("File type not allowed. Please upload PNG or JPG.", "error")
        return redirect(url_for("index"))

    # Save with a UUID to avoid collisions
    ext = file.filename.rsplit(".", 1)[1].lower()
    saved_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(config.UPLOAD_DIR, saved_name)
    file.save(save_path)

    try:
        predictions, top_idx = run_prediction(save_path)
    except Exception:
        log.exception("Prediction failed")
        flash("Something went wrong processing the image.", "error")
        return redirect(url_for("index"))

    gradcam_url = try_gradcam(save_path, top_idx)
    info = get_info(predictions[0]["class"])

    return render_template(
        "result.html",
        image_url=url_for("static", filename=f"uploads/{saved_name}"),
        gradcam_url=gradcam_url,
        predictions=predictions,
        top=predictions[0],
        info=info,
        demo_mode=DEMO_MODE,
    )


@app.route("/about")
def about():
    return render_template("about.html", demo_mode=DEMO_MODE)


# ---------- REST API ----------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    if "image" not in request.files:
        return jsonify({"error": "No 'image' field in multipart form."}), 400

    file = request.files["image"]
    if file.filename == "" or not is_allowed_file(file.filename):
        return jsonify({"error": "Invalid or missing image file."}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    saved_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(config.UPLOAD_DIR, saved_name)
    file.save(save_path)

    try:
        predictions, _ = run_prediction(save_path)
    except Exception as e:
        log.exception("API prediction failed")
        return jsonify({"error": "Prediction failed", "detail": str(e)}), 500

    top = predictions[0]
    return jsonify({
        "top_prediction": top["class"],
        "top_prediction_pretty": top["pretty"],
        "confidence": top["confidence"],
        "top_3": predictions,
        "disease_info": get_info(top["class"]),
        "demo_mode": DEMO_MODE,
    })


@app.route("/api/classes")
def api_classes():
    return jsonify({
        "num_classes": config.NUM_CLASSES,
        "classes": config.CLASS_NAMES,
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": MODEL is not None,
        "demo_mode": DEMO_MODE,
    })


@app.errorhandler(413)
def too_large(e):
    return jsonify({
        "error": f"File larger than {config.MAX_UPLOAD_SIZE_MB} MB."
    }), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)),
            debug=os.environ.get("FLASK_DEBUG", "0") == "1")
