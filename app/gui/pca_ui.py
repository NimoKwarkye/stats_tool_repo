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
            with dpg.tab(label="data", tag=self.data_window):
                with dpg.tree_node(label="Data Import"):
                    dpg.add_button(label="...", 
                                    callback=lambda: constants.file_dialog(self.import_data),
                                    pos=constants.set_relative_pos(self.data_window, "h_center"))
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
        file_path =  app_data["selections"][list(app_data["selections"].keys())[0]]
        self.data = csv.read_data_pca(file_path, "g")

        with dpg.table(header_row=True, resizable=True, 
                            tag=self.cur_displayed_data, 
                            parent=self.data_window, row_background=True,
                            borders_innerH=True, borders_outerH=True, 
                            borders_innerV=True,
                            borders_outerV=True, delay_search=True):
        # Add columns
            for feature in self.data["features"]:
                dpg.add_table_column(label=feature)

            # Add rows
            for row in self.data["data"]:
                with dpg.table_row():
                    for cell in row:
                        dpg.add_text(f"{cell:.4f}")
            with dpg.table_row():
                for i in range(len(self.data["features"])):
                    mn = self.data["data"][:, i].mean()
                    std = self.data["data"][:, i].std()
                    dpg.add_text(f"mn = {mn:.2f}\nstd = {std:.2f}")

        #TODO add summary statistics
        dpg.add_separator(parent=self.data_window)
        gph.plot_correlation_map(self.data_window, self.data["data"], list(self.data["features"]))


def show():
    ui = PCA_ui()
    ui()