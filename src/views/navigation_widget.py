import os
import re
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QRadioButton, QButtonGroup, QPushButton
from PySide2.QtCore import Qt, Signal

from .create_project_widget import CreateProjectDialog
from .shots_nav_widget import ShotsNavWidget
from .assets_nav_widget import AssetsNavWidget

class NavigationWidget(QWidget):
    navigation_updated = Signal()
    def __init__(self, parent=None):
        super(NavigationWidget, self).__init__(parent)
        
        self.state = {
            'project_code': None,
            'nav_type': 'assets'
        }

        self.shots_state = {
            'project_code': None,
            'episode': None,
            'shot': None
        }

        self.assets_state = {
            'project_code': None,
            'asset_type': None,
            'asset': None
        }
        
        self.layout = QVBoxLayout()
        
        self.first_row_layout = QHBoxLayout()
        
        self.project_dropdown = QComboBox()
        self.project_dropdown.setEnabled(False)
        self.project_dropdown.currentIndexChanged.connect(self.on_project_selected)
        self.first_row_layout.addWidget(self.project_dropdown)
        
        self.radio_button_group = QButtonGroup(self)
        self.shots_radio = QRadioButton("Shots")
        self.assets_radio = QRadioButton("Assets")
        self.assets_radio.setChecked(True)
        self.radio_button_group.addButton(self.shots_radio)
        self.radio_button_group.addButton(self.assets_radio)
        self.shots_radio.toggled.connect(self.update_navigation_options)
        self.assets_radio.toggled.connect(self.update_navigation_options)
        self.first_row_layout.addWidget(self.shots_radio)
        self.first_row_layout.addWidget(self.assets_radio)
        
        self.layout.addLayout(self.first_row_layout)
        
        self.shots_nav_widget = ShotsNavWidget()
        self.assets_nav_widget = AssetsNavWidget()

        self.shots_nav_widget.navigation_updated.connect(self.on_navigation_updated)
        self.shots_nav_widget.entity_created.connect(self.on_entity_created)
        
        self.assets_nav_widget.navigation_updated.connect(self.on_navigation_updated)
        self.assets_nav_widget.entity_created.connect(self.on_entity_created)
        
        self.layout.addWidget(self.shots_nav_widget)
        self.layout.addWidget(self.assets_nav_widget)
        
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setFixedSize(24, 24)
        self.refresh_button.clicked.connect(self.update_project_path)
        self.layout.addWidget(self.refresh_button, alignment=Qt.AlignRight)
        
        self.setLayout(self.layout)
        
        self.update_project_path()

    def get_current_state(self):
        if self.state.get('nav_type') == 'assets':
            return self.assets_state
        else:
            return self.shots_state        

    def get_current_path(self):
        if self.state['nav_type'] == 'assets':
            current_state = self.assets_state
            base_path = os.path.join(os.getenv('PRTTM_PROJECTS_PATH'), current_state['project_code'], "Assets", current_state.get('asset_type', ''), current_state.get('asset', ''))
        else:
            current_state = self.shots_state
            base_path = os.path.join(os.getenv('PRTTM_PROJECTS_PATH'), current_state['project_code'], "Episodes", current_state.get('episode', ''), "shots", current_state.get('shot', ''))
        
        if not os.path.exists(base_path):
            QMessageBox.warning(self, "Path Not Found", "The specified path does not exist.")
            return None
        
        return base_path

    def open_current_path(self):
        current_path = self.get_current_path()
        if current_path:
            if sys.platform == 'win32':
                os.startfile(current_path)
            elif sys.platform == 'darwin':
                os.system(f'open "{current_path}"')
            else:
                os.system(f'xdg-open "{current_path}"')     
                
    def is_entity_selected(self):
        if self.state['nav_type'] == 'assets':
            return bool(self.assets_state['asset'])
        else:
            return bool(self.shots_state['shot'])                   

    def update_project_path(self):
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        if project_path and os.path.isdir(project_path):
            self.set_controls_enabled(True)
            self.update_project_dropdown()
            self.restore_state()
        else:
            self.set_controls_enabled(False)
            return

    def set_controls_enabled(self, enabled):
        self.project_dropdown.setEnabled(enabled)
        self.shots_radio.setEnabled(enabled)
        self.assets_radio.setEnabled(enabled)
        self.refresh_button.setEnabled(enabled)
        self.update_navigation_options()

    def update_project_dropdown(self):
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        if project_path:
            self.populate_dropdown(self.project_dropdown, self.get_valid_project_folders(project_path))
        
    def populate_dropdown(self, dropdown, items):
        dropdown.clear()
        dropdown.addItem("<select one>")
        dropdown.addItem("Create New")
        for item in sorted(items):
            dropdown.addItem(item)

    def get_valid_project_folders(self, path):
        valid_pattern = re.compile(r'^[A-Z0-9]{4}$')
        return [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder)) and valid_pattern.match(folder)]
            
    def on_project_selected(self, index):
        if index > 0:
            selected_text = self.project_dropdown.currentText()
            if selected_text == "Create New":
                self.create_new_project()
            else:
                self.state['project_code'] = selected_text
                self.shots_nav_widget.set_project(selected_text)
                self.assets_nav_widget.set_project(selected_text)
                self.update_navigation_options()
        else:
            self.state['project_code'] = None
            self.shots_nav_widget.reset()
            self.assets_nav_widget.reset()

    def create_new_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec_():
            self.update_project_path()

    def update_navigation_options(self):
        if self.assets_radio.isChecked():
            self.state['nav_type'] = 'assets'
            self.shots_nav_widget.hide()
            self.assets_nav_widget.show()
        else:
            self.state['nav_type'] = 'shots'
            self.assets_nav_widget.hide()
            self.shots_nav_widget.show()

    def restore_state(self):
        print("Restoring state:", self.state)
        
        def set_dropdown_value(dropdown, value):
            index = dropdown.findText(value)
            if index != -1:
                dropdown.setCurrentIndex(index)
        
        set_dropdown_value(self.project_dropdown, self.state['project_code'])
        if self.state['nav_type'] == 'assets':
            self.assets_radio.setChecked(True)
        else:
            self.shots_radio.setChecked(True)

    def on_navigation_updated(self, state):
        if self.state['nav_type'] == 'assets':
            self.assets_state.update(state)
        else:
            self.shots_state.update(state)
        print("Navigation Updated:", state)
        self.navigation_updated.emit()

    def on_entity_created(self, state):
        if self.state['nav_type'] == 'assets':
            self.assets_state.update(state)
            self.assets_nav_widget.reset()
            self.assets_nav_widget.set_project(self.assets_state['project_code'])
            self.assets_nav_widget.set_asset_type(self.assets_state.get('asset_type', ''))
        else:
            self.shots_state.update(state)
            self.shots_nav_widget.reset()
            self.shots_nav_widget.set_project(self.shots_state['project_code'])
            self.shots_nav_widget.set_episode(self.shots_state.get('episode', ''))
        print("Entity Created:", state)
        self.navigation_updated.emit()
