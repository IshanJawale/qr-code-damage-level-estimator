"""
QR Code Damage Level Inference
"""

import os
import numpy as np
import cv2
import torch
import torch.nn as nn
from typing import Union, Tuple, Dict


class TinyQRNet(nn.Module):
    """Tiny CNN for QR damage classification"""
    def __init__(self, num_classes=5):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(256, num_classes)
    
    def forward(self, x):
        z = self.features(x).flatten(1)
        return self.head(z)


class QRDamagePredictor:
    """QR damage level predictor"""
    
    CLASS_NAMES = {
        0: "Pristine",
        1: "Mild",
        2: "Moderate",
        3: "Heavy",
        4: "Severe"
    }
    
    def __init__(self, model_path: str, img_size: int = 160):
        self.img_size = img_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.model = TinyQRNet(num_classes=5)
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint)
        self.model.to(self.device)
        self.model.eval()
    
    def preprocess_image(self, image: np.ndarray) -> torch.Tensor:
        """Preprocess image for model input"""
        if len(image.shape) == 3:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            img = image
        
        img = cv2.resize(img, (self.img_size, self.img_size))
        img_normalized = img.astype(np.float32) / 255.0
        img_3ch = np.stack([img_normalized] * 3, axis=0)
        return torch.from_numpy(img_3ch).unsqueeze(0)
    
    def predict(self, image: Union[str, np.ndarray]) -> Dict:
        """Predict damage level"""
        if isinstance(image, str):
            img = cv2.imread(image)
        else:
            img = image
        
        tensor = self.preprocess_image(img).to(self.device)
        
        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=1)
            pred_class = logits.argmax(1).item()
            confidence = probs[0, pred_class].item()
        
        all_probs = {self.CLASS_NAMES[i]: probs[0, i].item() for i in range(5)}
        
        return {
            'class_id': pred_class,
            'class_name': self.CLASS_NAMES[pred_class],
            'confidence': confidence,
            'probabilities': all_probs
        }


if __name__ == "__main__":
    predictor = QRDamagePredictor("model/qr_damage_best.pt")
    print("Model loaded successfully!")
