import os
from PySide2.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide2.QtCore import Qt, Signal

from .create_episode_widget import CreateEpisodeDialog
from .create_shot_widget import CreateShotDialog

class ShotsNavWidget(QWidget):
    navigation_updated = Signal(dict)
    entity_created = Signal(dict)
    
    def __init__(self, parent=None):
        super(ShotsNavWidget, self).__init__(parent)
        
        self.state = {
            'project_code': None,
            'episode': None,
            'shot': None
        }
        
        self.layout = QVBoxLayout()
        
        self.episode_label = QLabel("Episodes:")
        self.layout.addWidget(self.episode_label)
        self.episode_dropdown = QComboBox()
        self.episode_dropdown.setEnabled(False)
        self.episode_dropdown.currentIndexChanged.connect(self.on_episode_selected)
        self.layout.addWidget(self.episode_dropdown)
        
        self.shot_label = QLabel("Shots:")
        self.layout.addWidget(self.shot_label)
        self.shot_dropdown = QComboBox()
        self.shot_dropdown.setEnabled(False)
        self.shot_dropdown.currentIndexChanged.connect(self.on_shot_selected)
        self.layout.addWidget(self.shot_dropdown)
        
        self.setLayout(self.layout)
    
    def reset(self):
        self.episode_dropdown.clear()
        self.episode_dropdown.setEnabled(False)
        self.shot_dropdown.clear()
        self.shot_dropdown.setEnabled(False)

    def set_project(self, project_code):
        self.state['project_code'] = project_code
        self.update_episode_dropdowns()

    def set_episode(self, episode):
        self.state['episode'] = episode
        self.update_shot_dropdown()

    def set_shot(self, shot):
        self.state['shot'] = shot

    def on_episode_selected(self, index):
        if index == 0:
            self.state['episode'] = None
            self.shot_dropdown.clear()
            self.shot_dropdown.setEnabled(False)
            self.navigation_updated.emit(self.state)
        else:
            selected_text = self.episode_dropdown.currentText()
            if selected_text == "Create New":
                self.create_new_episode()
            else:
                self.state['episode'] = selected_text
                self.update_shot_dropdown()
                self.navigation_updated.emit(self.state)

    def on_shot_selected(self, index):
        if index == 0:
            self.state['shot'] = None
            self.navigation_updated.emit(self.state)
        else:
            selected_text = self.shot_dropdown.currentText()
            if selected_text == "Create New":
                self.create_new_shot()
            else:
                self.state['shot'] = selected_text
                self.navigation_updated.emit(self.state)

    def create_new_episode(self):
        dialog = CreateEpisodeDialog(self.state['project_code'], self)
        if dialog.exec_():
            self.update_episode_dropdowns()
            self.entity_created.emit(self.state)

    def create_new_shot(self):
        dialog = CreateShotDialog(self.state['project_code'], self.state['episode'], self)
        if dialog.exec_():
            self.update_shot_dropdown()
            self.entity_created.emit(self.state)

    def update_episode_dropdowns(self):
        project_path = os.path.join(os.getenv('PRTTM_PROJECTS_PATH'), self.state['project_code'], "Episodes")
        self.populate_dropdown(self.episode_dropdown, self.get_subfolders(project_path))
        self.episode_dropdown.setEnabled(True)

    def update_shot_dropdown(self):
        project_path = os.path.join(os.getenv('PRTTM_PROJECTS_PATH'), self.state['project_code'], "Episodes", self.state['episode'], "shots")
        self.populate_dropdown(self.shot_dropdown, self.get_subfolders(project_path))
        self.shot_dropdown.setEnabled(True)
    
    def populate_dropdown(self, dropdown, items):
        dropdown.clear()
        dropdown.addItem("<select one>")
        dropdown.addItem("Create New")
        for item in sorted(items):
            dropdown.addItem(item)

    def get_subfolders(self, path):
        return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))] if path and os.path.exists(path) else []
