import time
from typing import List, Tuple, Optional
import json
from detection_zone import DetectionZone, BottleSpec
from visualization import VisualizationManager

class BottleDetector:
    def __init__(self, detection_zone: DetectionZone, bottle_spec: BottleSpec):
        self.frame_count = 0
        self.detection_zone = detection_zone
        self.bottle_spec = bottle_spec
        self.visualizer = VisualizationManager()
        
    def get_frame(self):
        """Get frame from camera"""
        # In production: Replace with actual camera capture
        self.frame_count += 1
        # Simulate frame capture
        frame = self.visualizer.create_blank_frame()
        return frame
    
    def detect_bottles(self, frame) -> List[Tuple[float, float]]:
        """Detect bottles in frame and return their positions"""
        detected_bottles = []
        
        # In production: Implement actual computer vision detection
        # This simulation now generates multiple bottles
        bottles = self._simulate_multiple_detections()
        for bottle in bottles:
            if bottle and self.detection_zone.is_inside(bottle):
                detected_bottles.append(bottle)
            
        # Visualize detection
        self.visualizer.draw_detection_zone(frame, self.detection_zone)
        self.visualizer.draw_detected_bottles(frame, detected_bottles)
        self.visualizer.show_frame("PET Bottle Detector", frame)
        
        return detected_bottles
    
    def _simulate_multiple_detections(self) -> List[Tuple[float, float]]:
        """Simulate multiple bottle detections for testing"""
        bottles = []
        
        # Simulate 2-3 bottles at different positions
        base_x = (self.frame_count % 100) / 100.0
        
        # First bottle
        bottles.append((base_x, 0.3))
        
        # Second bottle slightly offset
        if base_x < 0.9:  # Ensure it's within bounds
            bottles.append((base_x + 0.1, 0.5))
        
        # Third bottle occasionally
        if self.frame_count % 3 == 0 and base_x < 0.8:
            bottles.append((base_x + 0.2, 0.7))
        
        return bottles
    
    def classify_pet(self, bottle_region) -> bool:
        """Classify if detected object is a PET bottle"""
        # Simulate bottle measurements
        height = 0.25  # meters
        width = 0.08   # meters
        area = height * width
        color_match = True  # In production: implement actual color matching
        
        return self.bottle_spec.validate_bottle(
            height=height,
            width=width,
            area=area,
            color_match=color_match
        )
    
    def update_bottle_spec(self, new_spec_json: str):
        """Update bottle specifications"""
        try:
            spec_dict = json.loads(new_spec_json)
            self.bottle_spec = BottleSpec.from_config(spec_dict)
            print("Bottle specifications updated successfully")
        except Exception as e:
            print(f"Error updating bottle specifications: {str(e)}")
            
    def get_current_spec(self) -> str:
        """Get current bottle specifications as JSON"""
        return self.bottle_spec.to_json()