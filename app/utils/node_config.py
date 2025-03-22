import dearpygui.dearpygui as dpg
from app.ui.data_import_nodeui import CSVImportNodeUI
from app.ui.regression_nodeui import SimpleLinearRegressionNodeUI, LinearRegressionNodeUI
from app.ui.data_import_nodeui import SQLDBImportNodeUI
from app.ui.plots_nodeui import HeatMapPlotNodeUI, XYScatterPlotNodeUI, PairGridPlotNodeUI
from app.ui.decomposition_nodeui import PCANodeUI, NMFNodeUI
from app.nodes.data_import_node import CSVImportNode, SQLDBImportNode
from app.nodes.linear_regression_node import SimpleLinearRegressionNode, LinearRegressionNode
from app.nodes.data_plots_nodes import HeatMapPlotNode, XYScatterPlotNode, PairGridPlotNode
from app.nodes.decomposition_nodes import PCANode, NMFNode
from app.nodes.clustering_nodes import KMeansNode, DBSCANNode
from app.ui.clustering_nodeui import KmeansNodeUI, DBSCANNodeUI
from app.nodes.classification_nodes import LogisticRegressionNode
from app.ui.classification_nodeui import LogisticRegressionNodeUI
from app.utils.constants import EDITOR_TAG, FUNCTIONS_PANEL_TAG, NODE_EDITOR_PANEL_TAG, \
                                NODE_EDITOR_TAG, OPENFILE_DIALOG_TAG, REF_NODE_TAG, CSVIMPORT_DRAG_ID, \
                                LINEAR_REG_DRAG_ID, SCATTER_PLOT_DRAG_ID,  LOG_WINDOW_TAG, \
                                SQLDB_IMPORT_DRAG_ID, HEATMAP_PLOT_DRAG_ID, SMP_LINEAR_REG_DRAG_ID, \
                                PCA_DRAG_ID, PAIR_GRID_PLOT_DRAG_ID, NMF_DRAG_ID, KMEANS_DRAG_ID, \
                                DBSCAN_DRAG_ID, LOGISTIC_REG_DRAG_ID 

NODE_CONFIG = {
    "CSVImportNode": {
        "drag_id": CSVIMPORT_DRAG_ID,
        "ui_class": CSVImportNodeUI,
        "node_class": CSVImportNode,
        "drag_text": "Add a New CSV Data Import Node",
        "drag_btn_name": "CSV Data Import",
        "prototype_id": f"proto_csv{dpg.generate_uuid()}",
        "category": "Data Import"
    },
    "SQLDBImportNode": {
        "drag_id": SQLDB_IMPORT_DRAG_ID,
        "ui_class": SQLDBImportNodeUI,
        "node_class": SQLDBImportNode,
        "drag_text": "Add a New SQL DB Import Node",
        "drag_btn_name": "SQL DB Import",
        "prototype_id": f"proto_sql_{dpg.generate_uuid()}",
        "category": "Data Import"
    },
    "SimpleLinearRegressionNode": {
        "drag_id": SMP_LINEAR_REG_DRAG_ID,
        "ui_class": SimpleLinearRegressionNodeUI,
        "node_class": SimpleLinearRegressionNode,
        "drag_text": "Add a Simple Linear Regression Node",
        "drag_btn_name": "Simple LR",
        "prototype_id": f"proto_smplr_{dpg.generate_uuid()}",
        "category": "Regression"
    },
    "LinearRegressionNode": {
        "drag_id": LINEAR_REG_DRAG_ID,
        "ui_class": LinearRegressionNodeUI,
        "node_class": LinearRegressionNode,
        "drag_text": "Add a Linear Regression Node",
        "drag_btn_name": "Linear Regression",
        "prototype_id": f"proto_linrg_{dpg.generate_uuid()}",
        "category": "Regression"
    },
    "HeatMapPlotNode": {
        "drag_id": HEATMAP_PLOT_DRAG_ID,
        "ui_class": HeatMapPlotNodeUI,
        "node_class": HeatMapPlotNode,
        "drag_text": "Add a HeatMap Plot Node",
        "drag_btn_name": "HeatMap Plot",
        "prototype_id": f"proto_heatmap_{dpg.generate_uuid()}",
        "category": "Plot"
    },
    "XYScatterPlotNode": {
        "drag_id": SCATTER_PLOT_DRAG_ID,
        "ui_class": XYScatterPlotNodeUI,
        "node_class": XYScatterPlotNode,
        "drag_text": "Add a XY Scatter Plot Node",
        "drag_btn_name": "XY Scatter Plot",
        "prototype_id": f"proto_scatter_plot_{dpg.generate_uuid()}",
        "category": "Plot"
    },
    "PCANode": {
        "drag_id": PCA_DRAG_ID,
        "ui_class": PCANodeUI,
        "node_class": PCANode,
        "drag_text": "Add a PCA Node",
        "drag_btn_name": "Principal Component Analysis",
        "prototype_id": f"proto_pca_{dpg.generate_uuid()}",
        "category": "Decomposition"
    },
    "PairGridPlotNode": {
        "drag_id": PAIR_GRID_PLOT_DRAG_ID,
        "ui_class": PairGridPlotNodeUI,
        "node_class": PairGridPlotNode,
        "drag_text": "Add a PairGrid Plot Node",
        "drag_btn_name": "PairGrid Plot",
        "prototype_id": f"proto_pairgrid_{dpg.generate_uuid()}",
        "category": "Plot"
    },
    "NMFNode": {
        "drag_id": NMF_DRAG_ID,
        "ui_class": NMFNodeUI,
        "node_class": NMFNode,
        "drag_text": "Add a NMF Node",
        "drag_btn_name": "Non-negative Matrix Factorization",
        "prototype_id": f"proto_nmf_{dpg.generate_uuid()}",
        "category": "Decomposition"
    },
    "KMeansNode": {
        "drag_id": KMEANS_DRAG_ID,
        "ui_class": KmeansNodeUI,
        "node_class": KMeansNode,
        "drag_text": "Add a KMeans Clustering Node",
        "drag_btn_name": "KMeans Clustering",
        "prototype_id": f"proto_kmeans_{dpg.generate_uuid()}",
        "category": "Clustering"
        },
    "DBSCANNode": {
        "drag_id": DBSCAN_DRAG_ID,
        "ui_class": DBSCANNodeUI,
        "node_class": DBSCANNode,
        "drag_text": "Add a DBSCAN Clustering Node",
        "drag_btn_name": "DBSCAN Clustering",
        "prototype_id": f"proto_dbscan_{dpg.generate_uuid()}",
        "category": "Clustering"
        },
    "LogisticRegressionNode": {
        "drag_id": LOGISTIC_REG_DRAG_ID,
        "ui_class": LogisticRegressionNodeUI,
        "node_class": LogisticRegressionNode,
        "drag_text": "Add a Logistic Regression Node",
        "drag_btn_name": "Logistic Regression",
        "prototype_id": f"proto_logreg_{dpg.generate_uuid()}",
        "category": "Classification"
    }
}

PLOT_NODES = ["HeatMapPlotNode", "XYScatterPlotNode", "PairGridPlotNode"]