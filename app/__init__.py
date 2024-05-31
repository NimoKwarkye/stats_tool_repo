import dearpygui.dearpygui as dpg

dpg.create_context()

import app_gui as ui



def run():
    app = ui.App_Ui()
    app()    
    dpg.create_viewport(title="stats tool", width=900, height=700)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()