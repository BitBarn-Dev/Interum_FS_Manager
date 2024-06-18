# views/main_menu_bar/menu_bar_windows.py
import os
from .base_menu_bar import BaseMenuBar
from PySide2.QtWidgets import QAction, QApplication

class WindowsMenuBar(BaseMenuBar):
    def __init__(self, parent=None):
        super(WindowsMenuBar, self).__init__(parent)
        
        # Copy Projects Directory to Clipboard action
        copy_projects_dir_action = QAction("Copy Projects Directory to Clipboard", self)
        copy_projects_dir_action.triggered.connect(self.copy_projects_dir_to_clipboard)
        self.file_menu.addAction(copy_projects_dir_action)
    
    def copy_projects_dir_to_clipboard(self):
        projects_path = os.environ.get('PRTTM_PROJECTS_PATH', '')
        clipboard = QApplication.clipboard()
        clipboard.setText(projects_path)
