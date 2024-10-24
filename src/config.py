# System Configuration
CONVEYOR_SPEED = 3.0  # meters per second
CONVEYOR_WIDTH = 1.0  # meters
NUM_VALVES = 32
VALVE_SPACING = CONVEYOR_WIDTH / NUM_VALVES  # meters
CAMERA_FPS = 60
DETECTION_THRESHOLD = 0.85  # confidence threshold

# Detection Zone Configuration
DETECTION_ZONE = {
    'x1': 0.1,  # meters from left edge
    'x2': 0.9,  # meters from left edge
    'y1': 0.1,  # meters from top edge
    'y2': 0.9   # meters from top edge
}

# Bottle Parameters
BOTTLE_PARAMS = {
    'colors': [
        {'name': 'clear', 'hsv_lower': (0, 0, 200), 'hsv_upper': (180, 30, 255)},
        {'name': 'blue', 'hsv_lower': (100, 50, 50), 'hsv_upper': (130, 255, 255)},
        {'name': 'green', 'hsv_lower': (35, 50, 50), 'hsv_upper': (85, 255, 255)}
    ],
    'size_range': {
        'min_height': 0.15,  # meters
        'max_height': 0.35,  # meters
        'min_width': 0.05,   # meters
        'max_width': 0.15    # meters
    },
    'area_range': {
        'min_area': 0.007,   # square meters
        'max_area': 0.05     # square meters
    },
    'aspect_ratio': {
        'min': 2.0,          # height/width
        'max': 3.5
    }
}