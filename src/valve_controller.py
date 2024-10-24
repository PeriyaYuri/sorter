class ValveController:
    def __init__(self, num_valves):
        self.num_valves = num_valves
        self.valve_states = [False] * num_valves
    
    def activate_valve(self, valve_index, duration_ms):
        """Activate specific valve for given duration"""
        if 0 <= valve_index < self.num_valves:
            self.valve_states[valve_index] = True
            # In production: Add actual GPIO control for valves
            print(f"Valve {valve_index} activated for {duration_ms}ms")
    
    def deactivate_valve(self, valve_index):
        """Deactivate specific valve"""
        if 0 <= valve_index < self.num_valves:
            self.valve_states[valve_index] = False
            # In production: Add actual GPIO control for valves
            print(f"Valve {valve_index} deactivated")