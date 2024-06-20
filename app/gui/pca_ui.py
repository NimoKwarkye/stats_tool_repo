import dearpygui.dearpygui as dpg
from app.plot import app_graph as gph
from app import constants
from app.data import csv

class PCA_ui():
    def __init__(self):
        self.plot_window = None
        self.data : dict = {}
        self.data_window = dpg.generate_uuid()
        self.cur_displayed_data = dpg.generate_uuid()

    def __call__(self):
        self.main_tab()

    def main_tab(self):
        with dpg.tab(label="PCA", closable=True, parent=constants.PRIMARY_TAB):
            with dpg.table(header_row=False, resizable=True):
                dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window() as child_window_1:
                        self.side_panel()
                    with dpg.group():
                        self.plot_area()
                        constants.adjustable_separator(self.plot_window, height=3)
                        self.footer()
    
    def side_panel(self):
        with dpg.tab_bar():
            with dpg.tab(label="data", id=self.data_window):
                
                dpg.add_button(label="...", callback=lambda: constants.file_dialog(self.import_data))
            with dpg.tab(label="analysis"):
                pass
    
    def plot_area(self):
        with dpg.child_window(height=500, tag=constants.PLOT_WINDOW) as self.plot_window:
            #data_series = gph.Series_Data(xlabel="PC1", ylabel="PC2", plot_type="scatter")
            #self.graph = gph.Plot_Series(data_series)
            #self.graph()
            pass

    def footer(self):
        with dpg.child_window():
            dpg.add_text("Child Window 3")
    
    def import_data(self, sender, app_data):
        file_path =  app_data["file_path_name"]
        self.data = csv.read_data_pca(file_path, "g")
        print(self.data)

        with dpg.table(header_row=True, resizable=True, id=self.cur_displayed_data, parent=self.data_window):
        # Add columns
            for feature in self.data["features"]:
                dpg.add_table_column(label=feature)

            # Add rows
            for row in self.data["data"]:
                with dpg.table_row():
                    for cell in row:
                        dpg.add_text(f"{cell:.4f}")


def show():
    ui = PCA_ui()
    ui()