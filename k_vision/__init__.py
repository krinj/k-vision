# -*- coding: utf-8 -*-

"""
Import our names here.
"""


__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.0.0"

# Expose the Visual functions.
from k_vision.visual import generate_colors
from k_vision.visual import draw_regions
from k_vision.visual import pixelate_region
from k_vision.visual import draw_region_mask
from k_vision.visual import draw_bar
from k_vision.visual import draw_bar_segment
from k_vision.visual import safe_extract
from k_vision.visual import safe_implant
from k_vision.visual import safe_extract_with_region
from k_vision.visual import safe_implant_with_region
from k_vision.visual import grid


# Expose the Text functions.
from k_vision.text import write_into_region
from k_vision.text import write_at_position
from k_vision.text import write_anchored
from k_vision.text import label_region
from k_vision.text import raw_text
