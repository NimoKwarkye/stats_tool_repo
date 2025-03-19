
import os
import dearpygui.dearpygui as dpg
from app.utils import app_themes

from app.utils.constants import FONT_FILE, FONT_SIZE, FONT_TAG

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def absolute_path(relative_path: str) -> str:
    return os.path.normpath(os.path.join(ROOT_DIR, relative_path))

def load_init_file():
    dpg.configure_app(init_file=absolute_path("./config/init.ini"))


def get_examples_folder() -> str:
    return absolute_path("./examples").replace("\\", "/")

def on_exit():
    print("Application is terminating...")
    init_file = absolute_path("./config/dpg.ini").replace("\\", "/")
    print(init_file)
    
    dpg.save_init_file(file=init_file)

def load_fonts():
    with dpg.font_registry():
        dpg.add_font(absolute_path(FONT_FILE), FONT_SIZE, tag=FONT_TAG)

def init():
    load_init_file()
    load_fonts()
    dpg.bind_font(FONT_TAG)
    app_themes.init()
    #dpg.set_exit_callback(callback=lambda: on_exit())