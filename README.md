# QR Damage Level Estimation (CNN, Synthetic)

A compact, from-scratch deep learning project that trains a small CNN to classify the “damage level” of QR codes using a fully synthetic dataset. The notebook generates the dataset on disk, trains the model, evaluates performance, and runs single-image predictions.

Key properties:
- Strict class-0 policy: class 0 images are truly pristine (no corruption).
- Class-aware corruptions for classes 1–4 with strictly increasing severity.
- Fully synthetic data; no manual collection required.

## Classes and Labeling Policy

| Class | Description | Severity range (s) | Corruption policy |
|------:|-------------|--------------------|-------------------|
| 0 | pristine | s = 0.00 | none |
| 1 | mild | 0.05–0.25 | light blur/noise, mild JPEG/contrast jitter |
| 2 | moderate | 0.25–0.50 | adds salt & pepper, light occlusion, morphology, perspective |
| 3 | heavy | 0.50–0.75 | stronger versions of class 2 effects |
| 4 | severe | 0.75–1.00 | strongest effects, larger occlusions/perspective and compression |

Class is sampled first (balanced), then severity is sampled within the class range. This prevents “class 0” contamination by design.

## What’s in the Notebook

- Setup: Installs minimal dependencies on Colab.
- Data: Generates train/val/test splits to disk with CSV labels; includes a per-class preview grid.
- Model: Tiny CNN with global average pooling head (5-way classification).
- Train: Progress bar, validation metrics, best/last checkpoints.
- Evaluate: Test accuracy and confusion matrix.
- Predict: Utility to predict damage level on your own images.

## Quick Start (Colab)

1. Open the notebook `QR Damage Level Estimation (CNN).ipynb` in Google Colab (Runtime → Change runtime type → GPU recommended).
2. Run all cells in order:
   - Setup (pip installs)
   - Data generation (adjust sizes as needed)
   - Preview grid (sanity check per class)
   - Model definition and training
   - Evaluation (confusion matrix)
   - Prediction function (optional: upload your image and call `predict_image`)

Default dataset sizes (fast demo):
- Train: 5,000
- Val: 1,000
- Test: 1,000
Increase these for better accuracy if time/GPU allows.

## Dataset on Disk

Structure (created under `data/qr_damage/`):

```
data/qr_damage/
  train/
    0/ 1/ 2/ 3/ 4/      # class folders
  val/
    0/ 1/ 2/ 3/ 4/
  test/
    0/ 1/ 2/ 3/ 4/
  train_labels.csv
  val_labels.csv
  test_labels.csv
```

Each CSV includes: `filename,label,severity,error_correction,payload`.

## Training Outputs

Checkpoints are saved to `runs/`:
- `best.pt` — best validation accuracy
- `last.pt` — last epoch

Typical T4 runtime (demo sizes): a few minutes. Larger datasets/epochs will increase training time and lift accuracy.

## Customization

- Dataset size and image size: tune `TRAIN_SIZE`, `VAL_SIZE`, `TEST_SIZE`, `IMG_SIZE`.
- Realism: composite QRs on backgrounds and add illumination gradients.
- Calibration: optionally align labels to actual decodability using a decoder (e.g., `pyzbar`).
- Multi-task: jointly predict damage level and QR error-correction level (L/M/Q/H).

## Troubleshooting

- Class-0 contamination: The notebook enforces “no corruption” for class 0. If you see damage in class-0 previews, re-run generation after verifying the “Data generation” cells ran without edits.
- Slow I/O: Reduce dataset sizes or switch to `.jpg` with quality ~95 for faster writes.
- CUDA OOM: Lower batch size or image size.

## 🚀 Inference & Web Interface

### Web Application
A Flask-based web interface for easy QR code damage level prediction:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
python app.py
```

Open `http://127.0.0.1:5000` in your browser. Features:
- **Upload Image**: Drag & drop or select QR code images
- **Camera Capture**: Take photos directly using your device camera
- **Real-time Results**: Get instant damage level predictions with confidence scores
- **Detailed Analysis**: View probability distribution across all damage levels

### Python API
Use the inference module directly in your code:

```python
from inference import QRDamagePredictor

# Initialize predictor
predictor = QRDamagePredictor("model/qr_damage_best.pt")

# Predict on an image
result = predictor.predict_with_details("path/to/qr_code.png")
print(f"Damage Level: {result['class_name']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### Batch Processing
Process multiple images at once:

```bash
python batch_inference.py data/test -o results.csv
```

For detailed inference documentation, see [README_INFERENCE.md](README_INFERENCE.md).

## 📁 Project Structure

```
qr-code-damage-level-estimator/
├── model/
│   └── qr_damage_best.pt        # Trained model weights
├── data/                         # Training/validation/test datasets
├── train/
│   └── qr_damage_level_estimator.ipynb  # Training notebook
├── templates/                    # Web interface HTML
├── static/                       # CSS and assets
├── inference.py                  # Core inference module
├── app.py                       # Flask web application
├── batch_inference.py           # Batch processing script
└── requirements.txt             # Dependencies
```

## License

This project is provided as-is for educational and research use. Add your preferred license if you publish a repository.