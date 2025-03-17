import dearpygui.dearpygui as dpg
from datetime import datetime
from app.utils.constants import LOG_WINDOW_TAG

class LogHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LogHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  
            self.log_window_tag = LOG_WINDOW_TAG
            self.logs = []
            self.log_count = -1
            self.log_limit = 100
            self.initialized = True
    

    
    def add_log(self, log: str, msg_type:int=0):
        if self.log_count < 0:
            dpg.add_separator(parent=self.log_window_tag)
            self.log_count = 0

        if self.log_count >= self.log_limit:
            log_tag = self.logs.pop(0)
            dpg.delete_item(log_tag)
            dpg.delete_item(f"{log_tag}_sep")
            before_log = self.logs[-1]
            self.log_text(log, msg_type, log_tag, before_log)
            self.logs.append(log_tag)

        else:
            self.log_count += 1
            
            before_log = 0
            if self.log_count > 1:
                before_log = self.logs[-1]
            
            log_tag = f"{self.log_window_tag}_log_{self.log_count}"
            self.logs.append(log_tag)
            self.log_text(log, msg_type, log_tag, before_log)

    
    def log_text(self, log: str, msg_type:int, log_tag: str, before_log: str):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if msg_type == 0:
            display_log = f"[{now_str}]->[Task Completed]\n{log}"
            dpg.add_text(display_log, parent=self.log_window_tag, 
                            tag=log_tag,  before=before_log)
        
        elif msg_type > 0:
            display_log = f"[{now_str}]->[Warning]\n{log}"
            dpg.add_text(display_log, parent=self.log_window_tag, 
                            tag=log_tag, color=(255, 255, 0, 255), before=before_log)
        
        elif msg_type < 0:
            display_log = f"[{now_str}]->[Error]\n{log}"
            dpg.add_text(display_log, parent=self.log_window_tag, 
                            tag=log_tag, color=(255, 0, 0, 255), before=before_log)
        
        dpg.add_separator(parent=self.log_window_tag, tag=f"{log_tag}_sep", before=before_log)
    

    def clear_logs(self):
        for log in self.logs:
            dpg.delete_item(log)
            dpg.delete_item(f"{log}_sep")
        self.log_count = 0
        self.logs = []
