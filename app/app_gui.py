from typing import Any
import dearpygui as dpg

class App_Ui:
    def __init__(self, windowName, width, height):
        self.width = width
        self.height = height
        self.windowName = windowName
        dpg.create_context()
        dpg.create_viewport(title=self.windowName, width=self.width, height=self.height)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        with dpg.window(label=""):
            pass

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
    def __del__(self):
        dpg.destroy_context()
