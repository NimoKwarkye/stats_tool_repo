from app.utils.constants import FONT_FILE, FONT_SIZE, FONT_TAG

import os
import dearpygui.dearpygui as dpg

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def absolute_path(relative_path: str) -> str:
    return os.path.normpath(os.path.join(ROOT_DIR, relative_path))


def load_fonts():
    with dpg.font_registry():
        dpg.add_font(absolute_path(FONT_FILE), FONT_SIZE, tag=FONT_TAG)
