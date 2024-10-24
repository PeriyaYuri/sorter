import math
from config import CONVEYOR_SPEED, VALVE_SPACING

class TrajectoryCalculator:
    def __init__(self, distance_to_valves):
        self.distance_to_valves = distance_to_valves  # meters
    
    def calculate_valve_timing(self, bottle_position: Tuple[float, float]) -> Tuple[int, float]:
        """Calculate which valve to activate and when"""
        x, y = bottle_position
        
        # Time until bottle reaches valves
        time_to_valve = self.distance_to_valves / CONVEYOR_SPEED
        
        # Calculate which valve to activate
        valve_index = min(
            int(x / VALVE_SPACING),
            31  # Max 32 valves (0-31)
        )
        
        # Calculate precise timing
        activation_time = time_to_valve * 1000  # convert to milliseconds
        
        return valve_index, activation_time