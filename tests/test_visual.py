# -*- coding: utf-8 -*-

from unittest import TestCase

import cv2
import numpy as np
from k_util import Region, pather

from k_vision import visual


class TestVisual(TestCase):

    def setUp(self):
        pather.create("output")

    # ======================================================================================================================
    # Colors.
    # ======================================================================================================================

    def test_color_generator(self):
        """ Can generate n colors. """
        self.assertEqual(500, len(visual.generate_colors(500)))
        self.assertEqual(10, len(visual.generate_colors(10)))
        self.assertEqual(5, len(visual.generate_colors(5)))

    def test_color_generation_types(self):
        """ Check whether we can generate colors in numpy and regular format. """
        self.assertEqual(list, type(visual.generate_colors(5)))
        self.assertEqual(np.ndarray, type(visual.generate_colors(5, as_numpy=True)))

    def test_color_parameters(self):
        """ Check whether we can generate colors in numpy and regular format. """
        colors_control = visual.generate_colors(5)

        colors_normal = visual.generate_colors(5)
        colors_faded = visual.generate_colors(5, saturation=0.5)
        colors_dark = visual.generate_colors(5, brightness=0.5)
        colors_range = visual.generate_colors(5, hue_range=0.3)
        colors_range_with_offset = visual.generate_colors(5, hue_range=0.3, hue_offset=0.2)

        self.assertSequenceEqual(colors_control, colors_normal)
        self.assert_sequence_not_equal(colors_control, colors_faded)
        self.assert_sequence_not_equal(colors_control, colors_dark)
        self.assert_sequence_not_equal(colors_control, colors_range)
        self.assert_sequence_not_equal(colors_range, colors_range_with_offset)

    def assert_sequence_not_equal(self, s1, s2):
        with self.assertRaises(Exception):
            self.assertSequenceEqual(s1, s2)

    # ======================================================================================================================
    # Region Drawing.
    # ======================================================================================================================

    def test_draw_region(self):
        image, regions = self.create_image_and_regions()
        self.validate_image(visual.draw_regions(image, regions))
        self.validate_image(visual.draw_regions(image, regions, overlay=True, color=(255, 0, 0)))

    def test_pixelate_region(self):
        image, regions = self.create_image_and_regions()
        self.validate_image(visual.pixelate_region(image, regions))

    def test_mask_region(self):
        image, regions = self.create_image_and_regions()
        self.validate_image(visual.draw_region_mask(image, regions))

    @staticmethod
    def create_image_and_regions() -> (np.ndarray, Region):
        image = np.zeros((500, 500, 3), dtype=np.uint8)
        r0 = Region(50, 100, 50, 100)
        r1 = Region(-10, 10, -10, 10)
        r2 = Region(450, 550, 50, 100)
        r3 = Region(50, 100, 450, 550)
        r4 = Region(-10, 510, -10, 510)
        return image, [r0, r1, r2, r3, r4]

    def validate_image(self, image):
        self.assertEqual(np.ndarray, type(image))

    # ======================================================================================================================
    # Bars.
    # ======================================================================================================================

    def test_draw_bar(self):
        """ Able to call the draw bar function without errors. """
        image = np.zeros((500, 500, 3), dtype=np.uint8)
        visual.draw_bar(image, 1.0, x=10, y=100, width=100, height=20)
        visual.draw_bar(image, 0.0, x=10, y=100, width=100, height=20)
        visual.draw_bar(image, 0.5, x=10, y=100, width=100, height=20)

    # ======================================================================================================================
    # Cropping.
    # ======================================================================================================================

    def test_region_extraction(self):
        """ Check that we can use the extract region function, and able to plant that region back into the image. """
        image, regions = self.create_image_and_regions()
        for region in regions:
            extracted = visual.safe_extract_with_region(image, region)
            implanted = visual.safe_implant_with_region(image, extracted, region)
            self.validate_image(extracted)
            self.validate_image(implanted)

    # ======================================================================================================================
    # Test Draw Grid.
    # ======================================================================================================================

    def test_draw_grid(self):
        """ Draw the grid. """

        n = 16

        # Create n randomly colored images.
        random_colors = visual.generate_colors(n)
        images = [np.zeros((50, 50, 3), dtype=np.uint8) for _ in range(n)]
        for i in range(n):
            images[i][:, :] = random_colors[i]

        image = visual.grid(images)
        cv2.imwrite("output/grid_default.png", image)

        image = visual.grid(images, n_rows=2)
        cv2.imwrite("output/grid_rows.png", image)

        image = visual.grid(images, n_columns=3)
        cv2.imwrite("output/grid_cols.png", image)

        image = visual.grid(images, image_size=(15, 15),
                            inner_x_pad=0, inner_y_pad=0,
                            outer_pad=30,
                            bg_color=(30, 30, 30))
        cv2.imwrite("output/grid_small.png", image)

        image = visual.grid(images, image_size=(15, 15),
                            inner_x_pad=10, inner_y_pad=0,
                            outer_pad=15,
                            bg_color=(30, 30, 30))
        cv2.imwrite("output/grid_uneven.png", image)

        image = visual.grid(images, n_rows=2, n_columns=2)
        cv2.imwrite("output/grid_trunc.png", image)
