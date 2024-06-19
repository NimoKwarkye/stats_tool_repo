import dearpygui.dearpygui as dpg
from app.plot import app_graph as gph
from app import constants


def show():
    with dpg.tab(label="PCA", closable=True, parent=constants.PRIMARY_TAB):
        with dpg.table(header_row=False, resizable=True):
            dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
            dpg.add_table_column()
            with dpg.table_row():
                with dpg.child_window() as child_window_1:
                    dpg.add_text("Child Window 1")
                    dpg.add_button(label="PCA")
                with dpg.group():
                    with dpg.child_window(height=500, tag=constants.PLOT_WINDOW) as child_window_2:
                        data_series = gph.Series_Data(xlabel="PC1", ylabel="PC2", plot_type="scatter")
                        #self.graph = gph.Plot_Series(data_series)
                        #self.graph()
                    constants.adjustable_separator(child_window_2)
                    with dpg.child_window():
                        dpg.add_text("Child Window 3")