import time
import json
from config import (
    CAMERA_FPS, NUM_VALVES, 
    DETECTION_ZONE, BOTTLE_PARAMS
)
from bottle_detector import BottleDetector
from valve_controller import ValveController
from trajectory_calculator import TrajectoryCalculator
from detection_zone import DetectionZone, BottleSpec

class PhotoSeparator:
    def __init__(self):
        # Initialize detection zone and bottle specifications
        detection_zone = DetectionZone(
            x1=DETECTION_ZONE['x1'],
            x2=DETECTION_ZONE['x2'],
            y1=DETECTION_ZONE['y1'],
            y2=DETECTION_ZONE['y2']
        )
        bottle_spec = BottleSpec.from_config(BOTTLE_PARAMS)
        
        # Initialize components
        self.detector = BottleDetector(detection_zone, bottle_spec)
        self.valve_controller = ValveController(NUM_VALVES)
        self.trajectory_calc = TrajectoryCalculator(distance_to_valves=0.5)
        self.frame_interval = 1.0 / CAMERA_FPS
    
    def process_frame(self):
        """Process single frame from camera"""
        frame = self.detector.get_frame()
        bottles = self.detector.detect_bottles(frame)
        
        # Process all detected bottles in parallel
        pet_bottles = []
        for bottle_pos in bottles:
            if self.detector.classify_pet(bottle_pos):
                pet_bottles.append(bottle_pos)
        
        # Calculate and activate valves for all PET bottles
        if pet_bottles:
            valve_activations = {}  # {valve_index: max_duration}
            
            # Calculate valve timings for all bottles
            for bottle_pos in pet_bottles:
                valve_index, timing = self.trajectory_calc.calculate_valve_timing(bottle_pos)
                # Store the longest activation duration for each valve
                if valve_index not in valve_activations or timing > valve_activations[valve_index]:
                    valve_activations[valve_index] = timing
            
            # Activate all required valves
            for valve_index, duration in valve_activations.items():
                self.valve_controller.activate_valve(valve_index, duration_ms=50)
    
    def update_detection_params(self, params_json: str):
        """Update detection parameters during runtime"""
        try:
            self.detector.update_bottle_spec(params_json)
            print("Detection parameters updated successfully")
        except Exception as e:
            print(f"Error updating parameters: {str(e)}")
    
    def get_current_params(self) -> str:
        """Get current detection parameters"""
        return self.detector.get_current_spec()
    
    def run(self):
        """Main processing loop"""
        print("Starting PET bottle separator...")
        print(f"Conveyor speed: 3 m/s")
        print(f"Number of valves: {NUM_VALVES}")
        print(f"Camera FPS: {CAMERA_FPS}")
        print("\nCurrent detection parameters:")
        print(self.get_current_params())
        
        try:
            while True:
                cycle_start = time.time()
                self.process_frame()
                
                # Maintain consistent frame rate
                processing_time = time.time() - cycle_start
                if processing_time < self.frame_interval:
                    time.sleep(self.frame_interval - processing_time)
                
        except KeyboardInterrupt:
            print("\nStopping PET bottle separator...")

def main():
    separator = PhotoSeparator()
    separator.run()

if __name__ == "__main__":
    main()