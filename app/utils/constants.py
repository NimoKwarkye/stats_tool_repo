import dearpygui.dearpygui as dpg
from itertools import chain
from typing import Union

VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 600
VIEWPORT_TITLE = "Stats Tool"

FONT_SIZE = 18
FONT_FILE = "../assets/fonts/Roboto-Regular.ttf"
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

def set_relative_pos(tag:Union[int, str], pos:str)->list[int]:
    rect_size = dpg.get_item_rect_size(tag)
    rect_pos = dpg.get_item_pos(tag)

    if pos == "h_center":
        return [rect_size[0]/2 + rect_pos[0], -1]
    elif pos == "v_center":
        return [0, rect_size[1]/2 + rect_pos[1]]
    elif pos == "center":
        return [rect_size[0]/2 + rect_pos[0], rect_size[1]/2 + rect_pos[1]]

    return []

def auto_align(item, alignment_type: int, parent: Union[int, str], x_align: float = 0.5, y_align: float = 0.5):
    def _center_h(_s, _d, data):
        '''parent = dpg.get_item_parent(data[0])
        while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":
            parent = dpg.get_item_parent(parent)'''
        parent_width = dpg.get_item_rect_size(parent)[0]
        width = dpg.get_item_rect_size(data[0])[0]
        new_x = (parent_width // 2 - width // 2) * data[1] * 2
        dpg.set_item_pos(data[0], [new_x, dpg.get_item_pos(data[0])[1]])

    def _center_v(_s, _d, data):
        '''parent = dpg.get_item_parent(data[0])
        while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":
            parent = dpg.get_item_parent(parent)'''
        parent_width = dpg.get_item_rect_size(parent)[1]
        height = dpg.get_item_rect_size(data[0])[1]
        new_y = (parent_width // 2 - height // 2) * data[1] * 2
        dpg.set_item_pos(data[0], [dpg.get_item_pos(data[0])[0], new_y])

    if 0 <= alignment_type <= 2:
        with dpg.item_handler_registry():
            if alignment_type == 0:
                # horizontal only alignment
                dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
            elif alignment_type == 1:
                # vertical only alignment
                dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])
            elif alignment_type == 2:
                # both horizontal and vertical alignment
                dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
                dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])

        dpg.bind_item_handler_registry(item, dpg.last_container())
    
