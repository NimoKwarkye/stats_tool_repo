import dearpygui.dearpygui as dpg

dpg.create_context()

from app import gui 
from .constants import VIEWPORT_WIDTH, VIEWPORT_HEIGHT, VIEWPORT_TITLE, FONT_TAG
from .fonts import load_fonts



def run():
    load_fonts()
    dpg.bind_font(FONT_TAG)
    _appInstance = gui.start()
    dpg.create_viewport(title=VIEWPORT_TITLE, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
    initial_width  = dpg.get_viewport_client_width()
    initial_height = dpg.get_viewport_client_height()
    
    dpg.set_viewport_resize_callback(_appInstance.resize_callback)
    _appInstance.resize_callback("initial", (initial_width, initial_height))

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()