import os
from abc import ABC, abstractmethod

import cv2
import numpy as np


class RoadDamageDetector(ABC):
    """Abstract base class: har detector ko detect_damage() likhna zaroori hai."""

    def __init__(self, model_name, confidence_threshold=0.5):
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold

    @abstractmethod
    def detect_damage(self, image_bytes):
        pass


class MLRoadDamageDetector(RoadDamageDetector):
    """TFLite model se pothole / normal road classify karta hai."""

    def __init__(self, model_path):
        super().__init__("pothole_classifier.tflite")
        self.model_path = model_path
        self.detected_classes = ["Normal", "Pothole"]
        self._interpreter = None

    def _load_model(self):
        # TensorFlow sirf pehli prediction par import hota hai (startup tez rehta hai)
        if self._interpreter is not None:
            return
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("Model file nahi mili: " + self.model_path)
        import tensorflow as tf
        self._interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self._interpreter.allocate_tensors()
        self._input = self._interpreter.get_input_details()[0]["index"]
        self._output = self._interpreter.get_output_details()[0]["index"]

    def process_image(self, image_bytes):
        """OpenCV + NumPy: bytes -> array -> RGB -> 224x224 -> 0..1 -> batch."""
        data = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Ye valid image file nahi hai.")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = image.astype(np.float32) / 255.0
        return np.expand_dims(image, axis=0)

    def classify_damage(self, image_array):
        self._load_model()
        self._interpreter.set_tensor(self._input, image_array)
        self._interpreter.invoke()
        return float(self._interpreter.get_tensor(self._output)[0][0])

    def detect_damage(self, image_bytes):
        image_array = self.process_image(image_bytes)
        probability = self.classify_damage(image_array)
        if probability > self.confidence_threshold:
            label, confidence = "Pothole", probability * 100
        else:
            label, confidence = "Normal", (1 - probability) * 100
        return {"label": label, "confidence": round(confidence, 2)}
