# -*- coding: utf-8 -*-

"""
Library to do some cool visual stuff.
"""
import math
from typing import List
import cv2
import numpy as np
import colorsys

from k_util import Region

__author__ = "Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


# ======================================================================================================================
# Color Tools.
# ======================================================================================================================


def generate_colors(n,
                    saturation: float = 1.0,
                    brightness: float = 1.0,
                    hue_offset: float = 0.0,
                    hue_range: float = 1.0,
                    as_numpy: bool = False):
    """ Generate N amount of colors spread across a range on the HSV scale.
    Will return it in a numpy format. """
    hsv = [(hue_offset + hue_range * (i / n), saturation, brightness) for i in range(n)]
    colors_raw = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    colors = np.array(colors_raw)
    colors *= 255

    if not as_numpy:
        colors = [(int(c[0]), int(c[1]), int(c[2])) for c in colors]

    return colors


# ======================================================================================================================
# Region Drawing Tools.
# ======================================================================================================================


def draw_regions(image: np.array,
                 regions: List[Region],
                 color=(255, 255, 255),
                 thickness: int = 2,
                 overlay: bool = False,
                 strength: float = 1.0):
    """ Draw a bounding box around each region area."""
    overlay_image = np.zeros_like(image, np.uint8) if overlay else np.copy(image)

    for i in range(len(regions)):
        r = regions[i]
        cv2.rectangle(overlay_image, (r.left, r.top), (r.right, r.bottom),
                      color=color,
                      thickness=thickness)

    if overlay:
        image = cv2.addWeighted(image, 1.0, overlay_image, strength, 0.0)
    else:
        image = cv2.addWeighted(image, 1.0 - strength, overlay_image, strength, 0.0)

    return image

  
def pixelate_region(image: np.array, regions: List[Region], blur_factor: float = 0.1):
    """ Re-sample the area within the regions to be pixelated. """
    for r in regions:
        target_image = safe_extract(image, r.left, r.right, r.top, r.bottom)
        h = target_image.shape[0]
        w = target_image.shape[1]

        pixel_h = max(1, int(h * blur_factor))
        pixel_w = max(1, int(w * blur_factor))

        target_image = cv2.resize(target_image, (pixel_w, pixel_h),
                                  interpolation=cv2.INTER_NEAREST)
        target_image = cv2.resize(target_image, (w, h), interpolation=cv2.INTER_NEAREST)
        image = safe_implant(image, target_image, r.left, r.right, r.top, r.bottom)

    return image


def draw_region_mask(image: np.array, regions: List[Region], strength: float = 1.0):
    """ Apply a mask to the areas covered by the regions. """
    dark_image = image.astype(np.float)
    fade_factor = 1.0 - (0.7 * strength)
    dark_image *= fade_factor
    dark_image = dark_image.astype(np.uint8)

    # Copy the regions onto the dark image.
    for r in regions:
        avatar = safe_extract_with_region(image, r)
        dark_image = safe_implant_with_region(dark_image, avatar, r)

    return dark_image


# ===================================================================================================
# Image Arrangement.
# ===================================================================================================


def grid(
        images: List[np.ndarray],
        n_columns: int=-1,
        n_rows: int=-1,
        image_size: (int, int)=None,
        bg_color: (int, int, int)=(255, 255, 255),
        inner_x_pad: int=5,
        inner_y_pad: int=5,
        outer_pad: int=15
):
    """ Returns an image with each of the images in the sequence drawn in a grid.
    It will resize each image to the image_size, but will use the size of
    the first image if image_size is not provided.
    You can specify the number of rows or columns to draw. If left on -1, it will auto-scale.
    """

    assert(len(images) > 0)

    # Calculate each image size.
    if image_size is None:
        image_size = images[0].shape[:2]

    template_width = image_size[1]
    template_height = image_size[0]

    # Calculate the number of rows and columns.
    if n_rows <= 0 and n_columns <= 0:
        # Make a perfect square of the grid.
        n_rows = n_columns = math.ceil(math.sqrt(len(images)))

    elif n_rows <= 0:
        # Rows are specified, so find the columns.
        n_rows = math.ceil(len(images) / n_columns)

    elif n_columns <= 0:
        # Columns are specified, so find the rows.
        n_columns = math.ceil(len(images) / n_rows)

    # Now calculate the canvas size.
    width = 2 * outer_pad + (n_columns * (template_width + inner_x_pad)) - inner_x_pad
    height = 2 * outer_pad + (n_rows * (template_height + inner_y_pad)) - inner_y_pad

    # Create the canvas.
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    canvas[:, :] = bg_color

    # Draw the items.
    for i, image in enumerate(images):

        if i == n_rows * n_columns:
            # That's all we can fit.
            break

        row = i // n_columns
        col = i % n_columns

        resized_image = cv2.resize(image, (template_width, template_height))
        x = col * (template_width + inner_x_pad) + outer_pad
        y = row * (template_height + inner_y_pad) + outer_pad

        canvas[y:y+template_height, x:x+template_width] = resized_image

    return canvas


# ======================================================================================================================
# Progress (or custom) Bars.
# ======================================================================================================================


def draw_bar(image, progress: float, x: int, y: int, width: int, height: int,
             frame_color=(0, 0, 0), bar_color=(0, 150, 255)):
    """ Draw a rectangular bar, with the specified progress value filled out. """
    draw_bar_segment(image, 0.0, 1.0, x, y, width, height, frame_color)  # Frame
    draw_bar_segment(image, 0.0, progress, x, y, width, height, bar_color)  # Bar


def draw_bar_segment(image, p_start: float, p_end: float, x: int, y: int, width: int, height: int, color=(0, 150, 255)):
    """ Draw a segment of a bar, for example if we just wanted a start-end section.
    Starting point is the top left. """

    # Draw the bar.
    p_width = max(0.0, p_end - p_start)
    p_width = int(width * p_width)
    if p_width > 0:
        p_x = int(x + p_start * width)
        cv2.rectangle(image, (p_x, y), (p_x + p_width, y + height), color, thickness=-1)


# ===================================================================================================
# 2D Image Slice Helpers.
# ===================================================================================================


def _get_safe_bounds(near: int, far: int, max_bound: int) -> (int, int, int, int):
    """ Finds the near/far bounds (such as left, right) for a certain max bound (width, etc). """
    safe_near = max(0, near)
    safe_far = min(max_bound, far)
    near_excess = safe_near - near
    far_excess = far - safe_far
    return safe_near, safe_far, near_excess, far_excess


def safe_extract(image: np.array, left: int, right: int, top: int, bottom: int):
    """ Extract the specified area from the image, padding the over-cropped areas with black.
    Assumes a np.array (CV2 image) input format. """

    safe_left, safe_right, left_excess, right_excess = _get_safe_bounds(left, right, image.shape[1])
    safe_top, safe_bottom, top_excess, bottom_excess = _get_safe_bounds(top, bottom, image.shape[0])

    # Extract the image.
    extracted_image = image[safe_top:safe_bottom, safe_left:safe_right]

    # Get the extraction area.
    output_h = bottom - top
    output_w = right - left

    safe_h = safe_bottom - safe_top
    safe_w = safe_right - safe_left

    # Fill the excess area with black.
    filler = np.zeros((output_h, output_w, 3), dtype=np.uint8)
    insert_bottom = top_excess + safe_h
    insert_right = left_excess + safe_w
    filler[top_excess:insert_bottom, left_excess:insert_right] = extracted_image
    return filler


def safe_implant(dst_image: np.array, src_image: np.array, left: int, right: int, top: int, bottom: int):
    """ Plant the area from the src image into the dst image. """

    # Get the extraction area.
    safe_left, safe_right, left_excess, right_excess = _get_safe_bounds(left, right, dst_image.shape[1])
    safe_top, safe_bottom, top_excess, bottom_excess = _get_safe_bounds(top, bottom, dst_image.shape[0])

    s_bottom = top_excess + (safe_bottom - safe_top)
    s_right = left_excess + (safe_right - safe_left)

    if safe_bottom - safe_top > 0 and safe_right - safe_left > 0:
        # Prevent import/slicing into 0 size matrices.
        dst_image[safe_top:safe_bottom, safe_left:safe_right] = src_image[top_excess:s_bottom, left_excess:s_right]

    return dst_image


def safe_extract_with_region(image: np.array, region: Region) -> np.array:
    """ Extract the image area specified by the region. """
    return safe_extract(image, region.left, region.right, region.top, region.bottom)


def safe_implant_with_region(dst_image: np.array, src_image: np.array, region: Region) -> np.array:
    """ Plant the area from the src image into the dst image. """
    return safe_implant(dst_image, src_image, region.left, region.right, region.top, region.bottom)
