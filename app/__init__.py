import dearpygui.dearpygui as dpg

dpg.create_context()

from .import app_gui as ui
from .constants import VIEWPORT_WIDTH, VIEWPORT_HEIGHT, VIEWPORT_TITLE, FONT_TAG
from .fonts import load_fonts



def run():
    load_fonts()
    dpg.bind_font(FONT_TAG)
    app = ui.App_Ui()
    app()    
    dpg.create_viewport(title=VIEWPORT_TITLE, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()