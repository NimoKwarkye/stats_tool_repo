import dearpygui.dearpygui as dpg

PLOT_AREA_TAG         = "PlotArea"

def plot_setup():
    with dpg.window(tag=PLOT_AREA_TAG, 
                            label="Plots", 
                            no_close=True, 
                            no_collapse=True,
                            no_scrollbar=True,
                            no_scroll_with_mouse=True):
        with dpg.subplots(rows=2, columns=3, height=-1, width=-1):
            with dpg.plot(label="Plot 1", height=-1, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                with dpg.plot_axis(dpg.mvYAxis, label="y"):
                    dpg.add_line_series([], [], label="0.5 + 0.5 * sin(x)", tag="series_tag")
            
            with dpg.plot(label="Plot 2", height=-1, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                with dpg.plot_axis(dpg.mvYAxis, label="y"):
                    dpg.add_line_series([], [], label="0.5 + 0.5 * cos(x)", tag="cos_series_tag")
            
            with dpg.plot(label="Plot 3", height=-1, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y")
            
            with dpg.plot(label="Plot 4", height=-1, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y")
            
            with dpg.plot(label="Plot 5", height=-1, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y")
            
            with dpg.plot(label="Plot 6", height=-1, width=-1):
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y")