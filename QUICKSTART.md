# Quick Start

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Web Interface

```bash
python app.py
```
Open: http://127.0.0.1:5000

### Python API

```python
from inference import QRDamagePredictor

# Initialize predictor
predictor = QRDamagePredictor("model/qr_damage_best.pt")

# Method 1: Simple prediction
class_id, confidence, all_probs = predictor.predict("image.png")
print(f"Class: {class_id}, Confidence: {confidence:.2%}")

# Method 2: Detailed prediction
result = predictor.predict_with_details("image.png")
print(f"Damage Level: {result['class_name']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Description: {result['description']}")

# View all probabilities
for class_name, prob in result['all_probabilities'].items():
    print(f"  {class_name}: {prob:.2%}")
```

Run your script:
```bash
python your_script.py
```

### Option 3: Command Line Testing 💻

Test the inference module directly:

```bash
python inference.py
```

This will automatically test on the first available image in `data/test/`.

### Option 4: Batch Processing 📊

Process multiple images at once:

```bash
# Basic usage
python batch_inference.py data/test -o results.csv

# With custom model
python batch_inference.py images/ -o output.csv -m model/custom_model.pt

# Get help
python batch_inference.py --help
```

The script will:
- Process all images in the specified directory
- Save results to a CSV file
- Generate statistics summary
- Create an error log if any images fail

## Expected Output

### Web Interface
You'll see a colorful interface with:
- Upload and camera options
- Live preview of your image
- Results showing:
  - Damage level badge (color-coded)
  - Confidence percentage
  - Detailed description
  - Probability bars for all classes

### Python API
```
Model loaded from: model/qr_damage_best.pt
Using device: cuda:0

Prediction Results:
  Class: Moderate Damage (ID: 2)
  Confidence: 87.35%
  Description: Moderate damage with some salt & pepper noise or light occlusion.
  
  All Class Probabilities:
    Pristine: 2.15%
    Mild Damage: 5.23%
    Moderate Damage: 87.35%
    Heavy Damage: 4.89%
    Severe Damage: 0.38%
```

### Batch Processing
```
Found 1000 images to process
Loading model...
Model loaded from: model/qr_damage_best.pt
Processing images: 100%|████████████| 1000/1000 [01:23<00:00, 12.05it/s]

✓ Results saved to: results.csv
  Successfully processed: 1000 images

📊 Summary Statistics:
  Pristine: 203 (20.3%)
  Mild Damage: 198 (19.8%)
  Moderate Damage: 205 (20.5%)
  Heavy Damage: 201 (20.1%)
  Severe Damage: 193 (19.3%)
```

## Damage Level Reference

| Level | Class | Description | Typical Confidence |
|-------|-------|-------------|-------------------|
| 0 | **Pristine** | Perfect condition, no visible corruption | > 95% |
| 1 | **Mild Damage** | Light blur or noise, still readable | 70-95% |
| 2 | **Moderate Damage** | Noticeable corruption, may affect scanning | 60-90% |
| 3 | **Heavy Damage** | Significant damage, readability affected | 50-85% |
| 4 | **Severe Damage** | Extreme corruption, likely unreadable | 40-80% |

## Troubleshooting

### Model Not Found
**Error:** `Model file not found: model/qr_damage_best.pt`

**Solution:**
1. Check if the file exists in the `model/` directory
2. Train the model using the notebook first
3. Verify the path in your code matches the actual file location

### Camera Not Working
**Issue:** Camera doesn't open in web interface

**Solutions:**
1. Grant camera permissions in your browser
2. Use HTTPS (some browsers require it for camera access)
3. Try a different browser (Chrome/Firefox recommended)
4. Check browser console (F12) for error messages

### Import Errors
**Error:** `ModuleNotFoundError: No module named 'torch'`

**Solution:**
```bash
pip install -r requirements.txt
```

If issues persist:
```bash
pip install torch torchvision opencv-python pillow flask numpy
```

### Out of Memory (OOM)
**Error:** CUDA out of memory

**Solutions:**
1. Use CPU instead:
   ```python
   predictor = QRDamagePredictor("model/qr_damage_best.pt", device="cpu")
   ```
2. Close other applications using GPU
3. Process images one at a time

### Port Already in Use
**Error:** `Address already in use: Port 5000`

**Solution:**
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Slow Inference
**Issue:** Predictions take too long

**Solutions:**
1. Use GPU if available (automatic by default)
2. Check if CUDA is properly installed
3. Close other applications
4. Use batch processing for multiple images

## Network Access

### Access from Other Devices

1. Find your local IP address:
   - **Windows:** `ipconfig` (look for IPv4 Address)
   - **macOS/Linux:** `ifconfig` or `ip addr`

2. Make sure the app is running with `host='0.0.0.0'` (default in `app.py`)

3. Access from other devices on the same network:
   ```
   http://YOUR_LOCAL_IP:5000
   ```
   Example: `http://192.168.1.100:5000`

### Firewall

If you can't access from other devices:
1. Allow Python through your firewall
2. Allow port 5000 (or your custom port)

## Performance Tips

1. **GPU Acceleration:** Use CUDA if available (10-50x faster)
2. **Batch Processing:** Process multiple images together using `batch_inference.py`
3. **Image Size:** Smaller images process faster (model uses 160x160)
4. **Model Loading:** Initialize predictor once, reuse for multiple predictions

## Next Steps

1. ✅ Test with your own QR code images
2. ✅ Try both upload and camera capture
3. ✅ Explore the Python API for custom integration
4. ✅ Process your entire image dataset with batch inference
5. ✅ Customize the web interface styling in `static/style.css`

## Need Help?

- Check the detailed documentation: [README_INFERENCE.md](README_INFERENCE.md)
- Review the main README: [README.md](README.md)
- Inspect the code comments in `inference.py` and `app.py`
- Test with the sample dataset in `data/test/`

## Example Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the web app
python app.py

# 3. Open browser to http://127.0.0.1:5000

# 4. Upload a QR code image or use camera

# 5. Get instant results!
```

Happy predicting! 🎉
