# views/main_menu_bar/base_menu_bar.py

from PySide2.QtWidgets import QMenuBar, QMenu, QAction
from PySide2.QtCore import Signal
import os
import subprocess

class BaseMenuBar(QMenuBar):
    files_updated = Signal()    
    def __init__(self, parent=None):
        super(BaseMenuBar, self).__init__(parent)
        self.file_menu = self.addMenu("File")
        
        # Open Projects Folder action
        open_projects_folder_action = QAction("Open Projects Folder", self)
        open_projects_folder_action.triggered.connect(self.open_projects_folder)
        self.file_menu.addAction(open_projects_folder_action)
    
    def open_projects_folder(self):
        projects_path = os.environ.get('PRTTM_PROJECTS_PATH', '')
        if os.path.exists(projects_path):
            if os.name == 'nt':  # Windows
                os.startfile(projects_path)
            elif os.name == 'posix':  # Linux or Mac
                subprocess.Popen(['xdg-open', projects_path])
