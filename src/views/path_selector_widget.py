import os
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide2.QtCore import Signal, Property

class PathSelectorWidget(QWidget):
    path_updated = Signal(str)
    
    def __init__(self, parent=None):
        super(PathSelectorWidget, self).__init__(parent)
        
        self._project_path = ""
        
        self.layout = QHBoxLayout()
        
        self.path_line_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        
        self.layout.addWidget(self.path_line_edit)
        self.layout.addWidget(self.browse_button)
        
        self.setLayout(self.layout)
        
        self.browse_button.clicked.connect(self.browse_path)
        self.path_line_edit.textChanged.connect(self.on_path_changed)
        
    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.path_line_edit.setText(path)
    
    def on_path_changed(self, path):
        self.project_path = path
    
    def get_project_path(self):
        return self._project_path
    
    def set_project_path(self, path):
        if self._project_path != path:
            self._project_path = path
            self.path_line_edit.setText(path)
            os.environ['PRTTM_PROJECTS_PATH'] = path
            self.path_updated.emit(path)
    
    def set_path(self, path):
        self.set_project_path(path)
    
    project_path = Property(str, get_project_path, set_project_path, notify=path_updated)
