import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.configure_app(docking=True, docking_space=True)

from app.ui.node_editor import NodeEditor
from app.utils.constants import VIEWPORT_WIDTH, VIEWPORT_HEIGHT, VIEWPORT_TITLE, FONT_TAG
from app.utils import utils



def run():
    dpg.create_viewport(title=VIEWPORT_TITLE, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
    utils.init()
    editor = NodeEditor()
    editor()    

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()