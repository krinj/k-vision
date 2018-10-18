# -*- coding: utf-8 -*-

from unittest import TestCase
from PIL.ImageFont import FreeTypeFont
import numpy as np
from k_util import Region

from k_vision import text
from k_vision.text import TextManager


class TestText(TestCase):

    def setUp(self):
        self.image: np.ndarray = np.zeros((500, 500, 3), dtype=np.uint8)

    # ======================================================================================================================
    # Test Singleton.
    # ======================================================================================================================

    def test_initialize_manager(self):
        """ The singleton text manager can be initialized. """
        text.TextManager.instance()

    def test_can_load_font(self):
        """ We can load both fonts at varying sizes with no error. """
        text_manager: TextManager = text.TextManager.instance()
        self.assertEqual(FreeTypeFont, type(text_manager.get_font(text.FONT_DEFAULT, 42)))
        self.assertEqual(FreeTypeFont, type(text_manager.get_font(text.FONT_DEFAULT, 8)))
        self.assertEqual(FreeTypeFont, type(text_manager.get_font(text.FONT_ICON, 42)))
        self.assertEqual(FreeTypeFont, type(text_manager.get_font(text.FONT_ICON, 36)))

    def test_can_get_font_divisor(self):
        """ Is able to get a float divisor for a particular font. """
        text_manager: TextManager = text.TextManager.instance()
        self.assertEqual(float, type(text_manager.get_font_divisor(text.FONT_DEFAULT)))
        self.assertEqual(float, type(text_manager.get_font_divisor(text.FONT_ICON)))

    # ======================================================================================================================
    # Test Drawing Functions.
    # ======================================================================================================================

    def test_raw_text(self):
        """ Test that raw text and icons can be drawn without error, and that they return images. """
        self.validate(text.raw_text(self.image, "Hello World", x=0, y=0))
        self.validate(text.raw_icon(self.image, u"\uf007", x=0, y=0))
        self.validate(text.write_icon(self.image, u"\uf007", x=0, y=0))

    def test_region_rendering(self):
        """ Able to use text-region writing functions without fail. """
        region = Region(10, 100, 10, 100)

        # Test all the different branches of this function.
        self.validate(text.write_into_region(self.image, "Hell World", region))
        self.validate(text.write_into_region(self.image, "Hell World", region, overlay=True))
        self.validate(text.write_into_region(self.image, "Hell World", region, h_align=text.ALIGN_LEFT))
        self.validate(text.write_into_region(self.image, "Hell World", region, h_align=text.ALIGN_RIGHT))
        self.validate(text.write_into_region(self.image, "Hell World", region,
                                             icon=u"\uf007", show_region_outline=True))

        # Test Region edge cases.
        self.validate(text.write_into_region(self.image, "Hell World", Region(-50, 50, 450, 550), font_size=42))
        self.validate(text.write_into_region(self.image, "Hell World", Region(450, 550, -50, 50), font_size=42))

        # Test Region labelling.
        self.validate(text.label_region(self.image, "Hello World", region))
        self.validate(text.label_region(self.image, "Hello World", region, show_at_bottom=True))
        self.validate(text.label_region(self.image, "Hello World", region, inside=True))

    def test_position_writing(self):
        """ Text if we can use the position based text-writing without failure. """
        self.validate(text.write_at_position(self.image, "How are you?", x=0, y=0, width=300))
        self.validate(text.center_at_position(self.image, "Fine thanks. And yourself?", x=250, y=250))
        self.validate(text.left_at_position(self.image, "Not too bad.", x=50, y=50))

    def test_anchored_writing(self):
        """ Test that we can successfully write text into anchored positions. """
        self.validate(text.write_anchored(self.image, "Top Left",
                                          h_anchor=text.ALIGN_LEFT, v_anchor=text.ALIGN_TOP))
        self.validate(text.write_anchored(self.image, "Bot Right",
                                          h_anchor=text.ALIGN_RIGHT, v_anchor=text.ALIGN_BOTTOM))
        self.validate(text.write_anchored(self.image, "Center",
                                          h_anchor=text.ALIGN_CENTER, v_anchor=text.ALIGN_CENTER))

    # ======================================================================================================================
    # Private Support Functions
    # ======================================================================================================================

    def validate(self, text_output):
        """ Checks if the text output is a valid ndarray (an image). """
        self.assertEqual(np.ndarray, type(text_output))
