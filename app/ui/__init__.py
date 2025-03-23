import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.configure_app(docking=True, docking_space=True)

from app.ui.node_editor import NodeEditor
from app.utils.constants import VIEWPORT_WIDTH, VIEWPORT_HEIGHT, VIEWPORT_TITLE, FONT_TAG
from app.utils import utils



def run():
    logos = utils.return_logos()
    dpg.create_viewport(title=VIEWPORT_TITLE, 
                        width=VIEWPORT_WIDTH, 
                        height=VIEWPORT_HEIGHT,
                        small_icon=logos[0],
                        large_icon=logos[1])
    utils.init()
    editor = NodeEditor()
    editor()    

    dpg.setup_dearpygui()
    dpg.set_viewport_small_icon(logos[0])
    dpg.set_viewport_large_icon(logos[1])
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()