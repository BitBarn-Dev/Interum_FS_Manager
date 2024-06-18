import os
from PySide2.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide2.QtCore import Qt, Signal

from .create_asset_type_widget import CreateAssetTypeDialog
from .create_asset_widget import CreateAssetDialog

class AssetsNavWidget(QWidget):
    navigation_updated = Signal(dict)
    entity_created = Signal(dict)
    
    def __init__(self, parent=None):
        super(AssetsNavWidget, self).__init__(parent)
        
        self.state = {
            'project_code': None,
            'asset_type': None,
            'asset': None
        }
        
        self.layout = QVBoxLayout()
        
        self.asset_type_label = QLabel("Asset Types:")
        self.layout.addWidget(self.asset_type_label)
        self.asset_type_dropdown = QComboBox()
        self.asset_type_dropdown.setEnabled(False)
        self.asset_type_dropdown.currentIndexChanged.connect(self.on_asset_type_selected)
        self.layout.addWidget(self.asset_type_dropdown)
        
        self.asset_label = QLabel("Assets:")
        self.layout.addWidget(self.asset_label)
        self.asset_dropdown = QComboBox()
        self.asset_dropdown.setEnabled(False)
        self.asset_dropdown.currentIndexChanged.connect(self.on_asset_selected)
        self.layout.addWidget(self.asset_dropdown)
        
        self.setLayout(self.layout)
    
    def reset(self):
        self.asset_type_dropdown.clear()
        self.asset_type_dropdown.setEnabled(False)
        self.asset_dropdown.clear()
        self.asset_dropdown.setEnabled(False)

    def set_project(self, project_code):
        self.state['project_code'] = project_code
        self.update_asset_type_dropdowns()

    def set_asset_type(self, asset_type):
        self.state['asset_type'] = asset_type
        self.update_asset_dropdown()

    def set_asset(self, asset):
        self.state['asset'] = asset

    def on_asset_type_selected(self, index):
        if index == 0:
            self.state['asset_type'] = None
            self.asset_dropdown.clear()
            self.asset_dropdown.setEnabled(False)
            self.navigation_updated.emit(self.state)
        else:
            selected_text = self.asset_type_dropdown.currentText()
            if selected_text == "Create New":
                self.create_new_asset_type()
            else:
                self.state['asset_type'] = selected_text
                self.update_asset_dropdown()
                self.navigation_updated.emit(self.state)

    def on_asset_selected(self, index):
        if index == 0:
            self.state['asset'] = None
            self.navigation_updated.emit(self.state)
        else:
            selected_text = self.asset_dropdown.currentText()
            if selected_text == "Create New":
                self.create_new_asset()
            else:
                self.state['asset'] = selected_text
                self.navigation_updated.emit(self.state)

    def create_new_asset_type(self):
        dialog = CreateAssetTypeDialog(self.state['project_code'], self)
        if dialog.exec_():
            self.update_asset_type_dropdowns()
            self.entity_created.emit(self.state)

    def create_new_asset(self):
        dialog = CreateAssetDialog(self.state['project_code'], self.state['asset_type'], self)
        if dialog.exec_():
            self.update_asset_dropdown()
            self.entity_created.emit(self.state)

    def update_asset_type_dropdowns(self):
        project_path = os.path.join(os.getenv('PRTTM_PROJECTS_PATH'), self.state['project_code'], "Assets")
        self.populate_dropdown(self.asset_type_dropdown, self.get_subfolders(project_path))
        self.asset_type_dropdown.setEnabled(True)

    def update_asset_dropdown(self):
        if self.state['asset_type']:
            project_path = os.path.join(os.getenv('PRTTM_PROJECTS_PATH'), self.state['project_code'], "Assets", self.state['asset_type'])
            self.populate_dropdown(self.asset_dropdown, self.get_subfolders(project_path))
            self.asset_dropdown.setEnabled(True)
    
    def populate_dropdown(self, dropdown, items):
        dropdown.clear()
        dropdown.addItem("<select one>")
        dropdown.addItem("Create New")
        for item in sorted(items):
            dropdown.addItem(item)

    def get_subfolders(self, path):
        return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))] if path and os.path.exists(path) else []
