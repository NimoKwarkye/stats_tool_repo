import dearpygui.dearpygui as dpg
from app.utils.constants import (
    GITHUB_LIGHT_THEME,
    MATERIAL_DARK_THEME,
    MATERIAL_LIGHT_THEME,
    DPG_DARK_THEME,
    DPG_LIGHT_THEME,
)

def set_material_dark_theme():
    with dpg.theme(tag=MATERIAL_DARK_THEME) as theme_id:
        with dpg.theme_component(0):
            # Text colors (unchanged)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (153, 153, 153, 255))
            
            # Backgrounds
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (18, 18, 18, 255))      # Dark grey close to #121212
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (18, 18, 18, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (31, 31, 31, 255))
            
            # Borders
            dpg.add_theme_color(dpg.mvThemeCol_Border, (38, 38, 38, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            
            # Frames / Input fields
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (33, 33, 33, 255))
            # Using a subtle lighter grey when hovered and active
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (55, 55, 55, 204))  # ~80% opacity
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (55, 55, 55, 172))   # ~67% opacity
            
            # Title bars (grey style)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (50, 50, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (30, 30, 30, 130))
            
            # Menu bar
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (26, 26, 26, 255))
            
            # Scrollbars (unchanged or slightly adjusted if desired)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (33, 33, 33, 135))  # ~53% opacity
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (102, 102, 102, 204))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (128, 128, 128, 204))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (128, 128, 128, 255))
            
            # Check marks and sliders
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (128, 128, 128, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (128, 128, 128, 200))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (110, 110, 110, 153))
            
            # BUTTONS (grey instead of blue)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (90, 90, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (160, 160, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 100, 100, 255))
            
            # Headers (for collapsing sections, etc.)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (128, 128, 128, 79))             # ~31%
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (192, 192, 192, 204))       # ~80%
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (166, 166, 166, 255))
            
            # Separators
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (51, 51, 51, 158))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (128, 128, 128, 200))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (128, 128, 128, 255))
            
            # Resize grips
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (89, 89, 89, 43))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, (66, 66, 66, 171))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, (66, 66, 66, 242))
            
            # Tabs
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (51, 51, 51, 237))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (70, 70, 70, 204))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (55, 55, 55, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (18, 18, 18, 253))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (38, 38, 38, 255))
            
            # Docking and empty backgrounds
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (128, 128, 128, 56))
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, (18, 18, 18, 255))
            
            # Plots (keeping these mostly neutral)
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines, (153, 153, 153, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, (128, 128, 128, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (230, 179, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, (255, 115, 0, 255))
            
            # Tables
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (38, 38, 38, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (102, 102, 102, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (128, 128, 128, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (18, 18, 18, 0))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (26, 26, 26, 23))
            
            # Selection and drag-drop
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (128, 128, 128, 89))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, (128, 128, 128, 242))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, (128, 128, 128, 204))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, (179, 179, 179, 179))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, (51, 51, 51, 51))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (51, 51, 51, 89))
 

        

def set_github_light_grey_theme():
    with dpg.theme(tag=GITHUB_LIGHT_THEME):
        with dpg.theme_component(dpg.mvAll):
            # Window and background colors (GitHub light background: #F6F8FA)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (246, 248, 250, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (246, 248, 250, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (246, 248, 250, 255))
            
            # Text color (dark grey: approx #24292E)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (36, 41, 46, 255))
            
            # Border color (light grey)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (225, 225, 225, 255))
            
            # Frame background colors
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (245, 245, 245, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (235, 235, 235, 255))
            
            # Title bar colors
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (246, 248, 250, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (230, 230, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (246, 248, 250, 255))
            
            # Button colors
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (245, 245, 245, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (235, 235, 235, 255))
            
            # Header colors (for tree nodes, collapsing headers, etc.)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (245, 245, 245, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (235, 235, 235, 255))
            
            # Slider/Grab accent color (GitHub blue: #0366D6)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (3, 102, 214, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (3, 102, 214, 255))


def some_dark_theme():
    with dpg.theme(tag="Some_dark_theme") as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # Styles
            #dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 4, 4, category=dpg.mvThemeCat_Core)
            #dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4, 4, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, 4, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)

            # Colors
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (33, 33, 33), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (48, 48, 48), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200), category=dpg.mvThemeCat_Core)

    with dpg.theme() as disabled_theme:
        with dpg.theme_component(dpg.mvAll):
            # Styles

            # Colors
            dpg.add_theme_color(dpg.mvThemeCol_Text, (100, 100, 100), category=dpg.mvThemeCat_Core)
    
def set_material_grey_theme():
    with dpg.theme(tag=MATERIAL_LIGHT_THEME):
        with dpg.theme_component(dpg.mvAll):
            # Background color (Grey 50: #FAFAFA)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (250, 250, 250, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (250, 250, 250, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (250, 250, 250, 255))
            
            # Text color (Grey 900: #212121)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (33, 33, 33, 255))
            
            # Border color (Grey 300: #E0E0E0)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (224, 224, 224, 255))
            
            # Frame background colors
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (245, 245, 245, 255))  # Grey 100
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (238, 238, 238, 255))  # Grey 200
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (224, 224, 224, 255))  # Grey 300
            
            # Title bar colors
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (238, 238, 238, 255))  # Grey 200
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (224, 224, 224, 255))  # Grey 300
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (238, 238, 238, 255))  # Grey 200
            
            # Button colors
            dpg.add_theme_color(dpg.mvThemeCol_Button, (224, 224, 224, 255))  # Grey 300
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (189, 189, 189, 255))  # Grey 400
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (158, 158, 158, 255))  # Grey 500
            
            # Header colors (for tree nodes, collapsing headers, etc.)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (224, 224, 224, 255))  # Grey 300
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (189, 189, 189, 255))  # Grey 400
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (158, 158, 158, 255))  # Grey 500
            
            # Slider/Grab accent color (Grey 600: #757575)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (117, 117, 117, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (97, 97, 97, 255))  # Grey 700

def dpg_dark_theme():
    with dpg.theme(tag=DPG_DARK_THEME):
        with dpg.theme_component(0):
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (0.50 * 255, 0.50 * 255, 0.50 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (0.06 * 255, 0.06 * 255, 0.06 * 255, 0.94 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (0.08 * 255, 0.08 * 255, 0.08 * 255, 0.94 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow           , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (0.16 * 255, 0.29 * 255, 0.48 * 255, 0.54 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg                , (0.04 * 255, 0.04 * 255, 0.04 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive          , (0.16 * 255, 0.29 * 255, 0.48 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed       , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.51 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg              , (0.14 * 255, 0.14 * 255, 0.14 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg            , (0.02 * 255, 0.02 * 255, 0.02 * 255, 0.53 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab          , (0.31 * 255, 0.31 * 255, 0.31 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered   , (0.41 * 255, 0.41 * 255, 0.41 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive    , (0.51 * 255, 0.51 * 255, 0.51 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (0.24 * 255, 0.52 * 255, 0.88 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive       , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.31 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Separator              , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered       , (0.10 * 255, 0.40 * 255, 0.75 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive        , (0.10 * 255, 0.40 * 255, 0.75 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.20 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered      , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive       , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab                    , (0.18 * 255, 0.35 * 255, 0.58 * 255, 0.86 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive              , (0.20 * 255, 0.41 * 255, 0.68 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused           , (0.07 * 255, 0.10 * 255, 0.15 * 255, 0.97 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive     , (0.14 * 255, 0.26 * 255, 0.42 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.70 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg         , (0.20 * 255, 0.20 * 255, 0.20 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines              , (0.61 * 255, 0.61 * 255, 0.61 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered       , (1.00 * 255, 0.43 * 255, 0.35 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram          , (0.90 * 255, 0.70 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered   , (1.00 * 255, 0.60 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg          , (0.19 * 255, 0.19 * 255, 0.20 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong      , (0.31 * 255, 0.31 * 255, 0.35 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight       , (0.23 * 255, 0.23 * 255, 0.25 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg             , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt          , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.06 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget         , (1.00 * 255, 1.00 * 255, 0.00 * 255, 0.90 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight  , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.70 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg      , (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.20 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg       , (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg                 , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.07 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBg                  , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBorder              , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg                , (0.08 * 255, 0.08 * 255, 0.08 * 255, 0.94 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBorder            , (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendText              , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_TitleText               , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText               , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBg                  , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgActive            , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgHovered           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisGrid                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisText                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Selection               , (1.00 * 255, 0.60 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs              , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (50, 50, 50, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundHovered, (75, 75, 75, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundSelected, (75, 75, 75, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, (100, 100, 100, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (41, 74, 122, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Link, (61, 133, 224, 200), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkSelected, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Pin, (53, 150, 250, 180), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_PinHovered, (53, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelector, (61, 133, 224, 30), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelectorOutline, (61, 133, 224, 150), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridBackground, (50, 50, 50, 200), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridLine, (5, 5, 5, 200), category=dpg.mvThemeCat_Nodes)


def dpg_light_theme():
    with dpg.theme(tag=DPG_LIGHT_THEME) as theme_id:
        with dpg.theme_component(0):
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (0.60 * 255, 0.60 * 255, 0.60 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (0.94 * 255, 0.94 * 255, 0.94 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.98 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.30 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow           , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg                , (0.96 * 255, 0.96 * 255, 0.96 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive          , (0.82 * 255, 0.82 * 255, 0.82 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed       , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.51 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg              , (0.86 * 255, 0.86 * 255, 0.86 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg            , (0.98 * 255, 0.98 * 255, 0.98 * 255, 0.53 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab          , (0.69 * 255, 0.69 * 255, 0.69 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered   , (0.49 * 255, 0.49 * 255, 0.49 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive    , (0.49 * 255, 0.49 * 255, 0.49 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive       , (0.46 * 255, 0.54 * 255, 0.80 * 255, 0.60 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.31 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Separator              , (0.39 * 255, 0.39 * 255, 0.39 * 255, 0.62 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered       , (0.14 * 255, 0.44 * 255, 0.80 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive        , (0.14 * 255, 0.44 * 255, 0.80 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip             , (0.35 * 255, 0.35 * 255, 0.35 * 255, 0.17 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered      , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive       , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab                    , (0.76 * 255, 0.80 * 255, 0.84 * 255, 0.93 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive              , (0.60 * 255, 0.73 * 255, 0.88 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused           , (0.92 * 255, 0.93 * 255, 0.94 * 255, 0.99 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive     , (0.74 * 255, 0.82 * 255, 0.91 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.22 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg         , (0.20 * 255, 0.20 * 255, 0.20 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines              , (0.39 * 255, 0.39 * 255, 0.39 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered       , (1.00 * 255, 0.43 * 255, 0.35 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram          , (0.90 * 255, 0.70 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered   , (1.00 * 255, 0.45 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg          , (0.78 * 255, 0.87 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong      , (0.57 * 255, 0.57 * 255, 0.64 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight       , (0.68 * 255, 0.68 * 255, 0.74 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg             , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt          , (0.30 * 255, 0.30 * 255, 0.30 * 255, 0.09 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight  , (0.70 * 255, 0.70 * 255, 0.70 * 255, 0.70 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg      , (0.20 * 255, 0.20 * 255, 0.20 * 255, 0.20 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg       , (0.20 * 255, 0.20 * 255, 0.20 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg       , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBg        , (0.42 * 255, 0.57 * 255, 1.00 * 255, 0.13 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBorder    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg      , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.98 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBorder  , (0.82 * 255, 0.82 * 255, 0.82 * 255, 0.80 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendText    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_TitleText     , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText     , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBg        , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgActive  , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgHovered , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisGrid      , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisText      , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Selection     , (0.82 * 255, 0.64 * 255, 0.03 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundHovered, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundSelected, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, (100, 100, 100, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (248, 248, 248, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Link, (66, 150, 250, 100), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkHovered, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkSelected, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Pin, (66, 150, 250, 160), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_PinHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelector, (90, 170, 250, 30), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelectorOutline, (90, 170, 250, 150), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridBackground, (225, 225, 225, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridLine, (180, 180, 180, 100), category=dpg.mvThemeCat_Nodes)
        
def init():
    set_material_dark_theme()
    set_github_light_grey_theme()
    set_material_grey_theme()
    dpg_dark_theme()
    dpg_light_theme()
    some_dark_theme()
    
    dpg.bind_theme("Some_dark_theme")