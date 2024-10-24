from dataclasses import dataclass
from typing import Tuple, Dict, List
import json

@dataclass
class DetectionZone:
    x1: float
    x2: float
    y1: float
    y2: float
    
    def is_inside(self, point: Tuple[float, float]) -> bool:
        x, y = point
        return (self.x1 <= x <= self.x2) and (self.y1 <= y <= self.y2)

@dataclass
class BottleSpec:
    min_height: float
    max_height: float
    min_width: float
    max_width: float
    min_area: float
    max_area: float
    aspect_ratio_range: Tuple[float, float]
    color_ranges: List[Dict]

    @classmethod
    def from_config(cls, config):
        return cls(
            min_height=config['size_range']['min_height'],
            max_height=config['size_range']['max_height'],
            min_width=config['size_range']['min_width'],
            max_width=config['size_range']['max_width'],
            min_area=config['area_range']['min_area'],
            max_area=config['area_range']['max_area'],
            aspect_ratio_range=(
                config['aspect_ratio']['min'],
                config['aspect_ratio']['max']
            ),
            color_ranges=config['colors']
        )
    
    def to_json(self) -> str:
        return json.dumps({
            'size_range': {
                'min_height': self.min_height,
                'max_height': self.max_height,
                'min_width': self.min_width,
                'max_width': self.max_width
            },
            'area_range': {
                'min_area': self.min_area,
                'max_area': self.max_area
            },
            'aspect_ratio': {
                'min': self.aspect_ratio_range[0],
                'max': self.aspect_ratio_range[1]
            },
            'colors': self.color_ranges
        }, indent=2)

    def validate_bottle(self, height: float, width: float, area: float, color_match: bool) -> bool:
        if not (self.min_height <= height <= self.max_height):
            return False
        if not (self.min_width <= width <= self.max_width):
            return False
        if not (self.min_area <= area <= self.max_area):
            return False
        
        aspect_ratio = height / width
        if not (self.aspect_ratio_range[0] <= aspect_ratio <= self.aspect_ratio_range[1]):
            return False
            
        return color_match