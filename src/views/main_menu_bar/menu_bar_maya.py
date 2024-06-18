import os
import re
from .base_menu_bar import BaseMenuBar
from PySide2.QtWidgets import QAction, QDialog, QVBoxLayout, QMessageBox
from PySide2.QtCore import Signal
from maya import cmds
from views.save_as_dialog import SaveAsDialog
from views.publisher import Publisher  # Import the Publisher

class MayaMenuBar(BaseMenuBar):
    def __init__(self, parent=None):
        super(MayaMenuBar, self).__init__(parent)
        
        self.file_menu.addSeparator()
        
        # Save Iteration action
        save_iteration_action = QAction("Save Iteration", self)
        save_iteration_action.triggered.connect(self.save_iteration)
        self.file_menu.addAction(save_iteration_action)
        
        # Save As action
        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_as)
        self.file_menu.addAction(save_as_action)
        
        self.file_menu.addSeparator()
        
        # Publish action
        publish_action = QAction("Publish", self)
        publish_action.triggered.connect(self.open_publisher)
        self.file_menu.addAction(publish_action)
    
    def save_iteration(self):
        current_file = cmds.file(query=True, sceneName=True)
        if current_file:
            dir_name, file_name = os.path.split(current_file)
            match = re.match(r'(.+_v)(\d+)(\.\w+)', file_name)
            if match:
                prefix, version, suffix = match.groups()
                new_version = int(version) + 1
                new_file_name = f"{prefix}{new_version:03d}{suffix}"
            else:
                base_name, ext = os.path.splitext(file_name)
                new_file_name = f"{base_name}_v001{ext}"
            
            new_file_path = os.path.join(dir_name, new_file_name)
            cmds.file(rename=new_file_path)
            cmds.file(save=True)
            self.files_updated.emit()
        else:
            QMessageBox.warning(self, "Save Iteration", "No file currently open in Maya.")
    
    def save_as(self):
        dialog = SaveAsDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            selected_file = dialog.get_selected_file()
            if selected_file:
                cmds.file(rename=selected_file)
                cmds.file(save=True)
                self.files_updated.emit()
    
    def open_publisher(self):
        current_file = cmds.file(query=True, sceneName=True)
        if self.is_valid_workfile(current_file):
            dialog = Publisher(current_file, self)
            if dialog.exec_() == QDialog.Accepted:
                self.files_updated.emit()
        else:
            QMessageBox.warning(self, "Publish", "You are working out of the pipeline. Please ensure your file is in the correct tasks directory and follows the naming conventions.")
    
    def is_valid_workfile(self, file_path):
        if not file_path:
            return False
        
        projects_path = os.environ.get('PRTTM_PROJECTS_PATH', '')
        if not file_path.startswith(projects_path):
            return False
        
        dir_name, file_name = os.path.split(file_path)
        if "_sandbox" in dir_name:
            return False
        
        if "Assets" in file_path:
            match = re.match(r'^(.+)_([a-zA-Z]+)_(.+)_(\w+)_v(\d+)\.\w+$', file_name)
            if not match:
                return False
        elif "Episodes" in file_path:
            match = re.match(r'^(.+)_([\d]{4})_([A-Za-z0-9]+)_(\w+)_v(\d+)\.\w+$', file_name)
            if not match:
                return False
        else:
            return False
        
        return True
