import dearpygui.dearpygui as dpg
from itertools import chain


VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 600
VIEWPORT_TITLE = "Stats Tool"

FONT_SIZE = 18
FONT_FILE = "assets/fonts/Roboto-Regular.ttf"
FONT_TAG = dpg.generate_uuid()
PLOT_WINDOW = dpg.generate_uuid()
YAXIS_1 = dpg.generate_uuid()
XAXIS_1 = dpg.generate_uuid()
ANNOTATION_PLOT = dpg.generate_uuid()
PRIMARY_TAB = dpg.generate_uuid()



def adjustable_separator(child_window, width=3840, height=2, colour=(255, 255, 255, 50)):
        with dpg.texture_registry():
            data = list(chain.from_iterable([[c / 255 for c in colour] for _ in range(width*height)]))
            separator_texture = dpg.add_static_texture(width=width, height=height, default_value=data)
        separator = dpg.add_image(separator_texture)
        def clicked_callback():
            while dpg.is_mouse_button_down(0):
                y_pos = dpg.get_mouse_pos()[1]
                dpg.split_frame(delay=10)
                y_delta = y_pos - dpg.get_mouse_pos()[1]
                height = dpg.get_item_height(child_window) - y_delta
                if height < 1: height = 1
                dpg.configure_item(child_window, height=height)
        with dpg.item_handler_registry() as item_handler:
            dpg.add_item_clicked_handler(callback=clicked_callback)
        dpg.bind_item_handler_registry(item=separator, handler_registry=item_handler)

def file_dialog(callback):
    with dpg.file_dialog(label="Import Data", height=500, width=700, directory_selector=False, callback=callback):
        dpg.add_file_extension(".csv", color=(0, 255, 0, 255))
        dpg.add_file_extension(".*", color=(150, 150, 150, 255))