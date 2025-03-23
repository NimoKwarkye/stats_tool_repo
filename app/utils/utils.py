
import os
import dearpygui.dearpygui as dpg
from app.utils import app_themes
import json
from pathlib import Path

from app.utils.constants import FONT_FILE, FONT_SIZE, FONT_TAG

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def absolute_path(relative_path: str) -> str:
    return os.path.normpath(os.path.join(ROOT_DIR, relative_path))

def load_init_file():
    dpg.configure_app(init_file=absolute_path("./config/init.ini"))


def get_basename(path: str) -> str:
    normalized_path = path.replace("\\", "/")
    return Path(normalized_path).name


def get_examples_folder() -> str:
    return absolute_path("./examples")

def update_example_file_path():
    examples_folder = get_examples_folder()
    examples = [os.path.join(examples_folder,  f) for f in os.listdir(examples_folder) if f.endswith(".json")]
    for example in examples:
        with open(example, "r") as f:
            data = json.load(f)
            for node in data["nodes"]:
                if node["node_type"] == "CSVImportNode":
                    
                    filename = get_basename(node["params"]["filepath"])
                    node["params"]["filepath"] = os.path.join(examples_folder, "data", filename)
        
        with open(example, "w") as f:
            json.dump(data, f, indent=2)


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
    update_example_file_path()
    #dpg.set_exit_callback(callback=lambda: on_exit())