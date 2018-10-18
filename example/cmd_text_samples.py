#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
<Description>
"""

import os

import cv2
import numpy as np
from k_util import Region
from k_util.logger import Logger

import sys
sys.path.append("..")

from k_vision import text

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


def show_image(text_function):
    """ Decorator to copy the input image, process it, and then show it in a window. """

    def func_wrapper(original_image, text_display: str):
        new_image = np.copy(original_image)
        new_image = text_function(new_image, text_display)
        cv2.imshow("Text Demo", new_image)
        cv2.waitKey(-1)

    return func_wrapper


def create_region_with_padding(image: np.array, pad: int):
    region: Region = Region(left=pad, right=image.shape[1] - pad,
                            top=pad, bottom=image.shape[0] - pad)
    return region


# ======================================================================================================================
# Simple rendering.
# ======================================================================================================================


@show_image
def plain_text(image: np.array, display_text: str):
    """ Render a text straight onto the image at the x and y position. """
    return text.raw_text(image=image, text=display_text, x=0, y=0)


@show_image
def big_text(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  font_size=42)


@show_image
def small_text(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  font_size=12)

# ======================================================================================================================
# Region based text rendering.
# ======================================================================================================================

@show_image
def region_text(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  show_region_outline=True)


@show_image
def region_text_left(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  pad=15,
                                  h_align=text.ALIGN_LEFT,
                                  show_region_outline=True)


@show_image
def region_text_right(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  pad=15,
                                  h_align=text.ALIGN_RIGHT,
                                  show_region_outline=True)


@show_image
def region_with_bg(image: np.array, display_text: str):
    """ Write text into the specified region, with a solid BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  bg_color=(0, 0, 0))


@show_image
def region_with_clear_bg(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  bg_color=(0, 0, 0),
                                  bg_opacity=0.5)


# ======================================================================================================================
# Icons.
# ======================================================================================================================


@show_image
def icon_raw(image: np.array, display_text: str):
    return text.raw_icon(image, display_text, x=0, y=0, font_size=48)


@show_image
def inline_icon_left(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  icon=u"\uf447",
                                  pad=12,
                                  h_align=text.ALIGN_LEFT,
                                  show_region_outline=True)


@show_image
def inline_icon_center(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  icon=u"\uf447",
                                  pad=12,
                                  show_region_outline=True)


# ======================================================================================================================
# Location based anchoring.
# ======================================================================================================================


@show_image
def write_centered_position(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    return text.center_at_position(image=image, text=display_text, x=150, y=100, pad=15, bg_color=(0, 0, 0))


@show_image
def write_left_aligned_position(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    return text.left_at_position(image=image, text=display_text, x=0, y=100, pad=15, bg_color=(0, 0, 0))


@show_image
def write_anchored_top_left(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    return text.write_anchored(image=image, text=display_text, h_anchor=text.ALIGN_LEFT, v_anchor=text.ALIGN_TOP,
                               pad=15, bg_color=(0, 0, 0))


@show_image
def write_anchored_center(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    return text.write_anchored(image=image, text=display_text, h_anchor=text.ALIGN_CENTER, v_anchor=text.ALIGN_CENTER,
                               pad=15, bg_color=(0, 0, 0))


@show_image
def write_anchored_bottom_right(image: np.array, display_text: str):
    """ Write text into the specified region, with a transparent BG. """
    return text.write_anchored(image=image, text=display_text, h_anchor=text.ALIGN_RIGHT, v_anchor=text.ALIGN_BOTTOM,
                               pad=15, bg_color=(0, 0, 0))


# ======================================================================================================================
# Overlay.
# ======================================================================================================================

@show_image
def overlay_text(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = create_region_with_padding(image, 15)
    return text.write_into_region(image=image,
                                  text=display_text,
                                  region=region,
                                  color=(0, 255, 0),
                                  overlay=True)


# ======================================================================================================================
# Region Labels.
# ======================================================================================================================


@show_image
def region_label(image: np.array, display_text: str):
    """ Write text into the specified region, with the anchor. """
    region = Region(100, 320, 40, 130)
    cv2.rectangle(image, (region.left, region.top), (region.right, region.bottom), color=(0, 255, 0), thickness=1)
    return text.label_region(image=image, text=display_text, region=region, icon=u"\uf447", show_at_bottom=True)

# ======================================================================================================================
# Run the script.
# ======================================================================================================================


if __name__ == "__main__":
    Logger.header("Running Text_Example")

    # Load the default image to draw on.
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, "stars.jpeg")
    print(file_path)
    base_image = cv2.imread(file_path)

    plain_text(base_image, "Plain Text")
    big_text(base_image, "BIG TEXT")
    small_text(base_image, "small text")
    region_text_left(base_image, "Region Left")
    region_text_right(base_image, "Region Right")
    region_with_bg(base_image, "Region With BG")
    region_with_clear_bg(base_image, "Clear BG")
    icon_raw(base_image, u"\uf447")
    inline_icon_left(base_image, "Left Inline Icon")
    inline_icon_center(base_image, "Center Inline Icon")
    write_centered_position(base_image, "Centered at Position")
    write_left_aligned_position(base_image, "Left Aligned at Position")
    overlay_text(base_image, "Overlay Text")

    write_anchored_top_left(base_image, "Top Left Anchored")
    write_anchored_center(base_image, "Center Anchored")
    write_anchored_bottom_right(base_image, "Bottom Right Anchored")
    region_label(base_image, "Region Label")

    cv2.destroyAllWindows()
