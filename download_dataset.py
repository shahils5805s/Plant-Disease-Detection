"""
Download the PlantVillage dataset from Kaggle.

Prerequisites:
  1. pip install kaggle
  2. Get your API token from https://www.kaggle.com/settings/account
     (click "Create New Token" → downloads kaggle.json)
  3. Place kaggle.json at ~/.kaggle/kaggle.json
     (Windows: C:\\Users\\<you>\\.kaggle\\kaggle.json)
  4. chmod 600 ~/.kaggle/kaggle.json  (Linux/macOS)

Then:
  python download_dataset.py
"""
import os
import shutil
import sys
import zipfile
from pathlib import Path

import config

DATASET = "abdallahalidev/plantvillage-dataset"
TARGET_DIR = Path(config.BASE_DIR) / "data"


def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        sys.exit(
            "kaggle package not installed. Run: pip install kaggle\n"
            "Then place kaggle.json in ~/.kaggle/"
        )

    api = KaggleApi()
    api.authenticate()

    print(f"[+] Downloading {DATASET} to {TARGET_DIR} …")
    api.dataset_download_files(DATASET, path=str(TARGET_DIR), unzip=True)
    print("[✓] Download complete.")

    # PlantVillage archives commonly contain a nested 'plantvillage dataset'
    # folder with color / grayscale / segmented subfolders. Normalise to
    # data/PlantVillage/<class>/*.jpg using the 'color' variant.
    color_dir = _find_color_dir(TARGET_DIR)
    if color_dir is None:
        print("[!] Could not auto-detect 'color' subfolder. Please rearrange")
        print(f"    images into {config.DATA_DIR}/<class_name>/*.jpg manually.")
        return

    print(f"[+] Detected color images at {color_dir}")
    final_dir = Path(config.DATA_DIR)
    if final_dir.exists():
        shutil.rmtree(final_dir)
    shutil.copytree(color_dir, final_dir)
    print(f"[✓] Copied into {final_dir}")
    print(f"[✓] Ready. {sum(1 for _ in final_dir.iterdir() if _.is_dir())} classes found.")


def _find_color_dir(root: Path):
    for path in root.rglob("*"):
        if path.is_dir() and path.name.lower() == "color":
            return path
    # Fallback: any folder that contains ~38 subfolders
    for path in root.rglob("*"):
        if path.is_dir():
            subs = [p for p in path.iterdir() if p.is_dir()]
            if 30 <= len(subs) <= 45:
                return path
    return None


if __name__ == "__main__":
    main()
