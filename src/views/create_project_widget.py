import os
import re
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

class CreateProjectDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateProjectDialog, self).__init__(parent)
        
        self.setWindowTitle("Create New Project")
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Enter new project code:")
        layout.addWidget(self.label)
        
        self.project_code_input = QLineEdit()
        self.project_code_input.textChanged.connect(self.sanity_check)
        layout.addWidget(self.project_code_input)
        
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.create_project)
        self.ok_button.setEnabled(False)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.help_button = QPushButton("?")
        self.help_button.clicked.connect(self.show_help)
        button_layout.addWidget(self.help_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def sanity_check(self):
        project_code = self.project_code_input.text()
        valid_pattern = re.compile(r'^[A-Z0-9]{4}$')
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if valid_pattern.match(project_code) and project_path:
            project_full_path = os.path.join(project_path, project_code)
            if not os.path.exists(project_full_path):
                self.ok_button.setEnabled(True)
                return
        self.ok_button.setEnabled(False)

    def show_help(self):
        QMessageBox.information(self, "Project Code Rules", "Project code must be exactly 4 characters long and can only contain uppercase letters and numbers (e.g., ABC1). The folder must not already exist.")
    
    def create_project(self):
        project_code = self.project_code_input.text()
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if project_path:
            project_full_path = os.path.join(project_path, project_code)
            try:
                os.makedirs(project_full_path)
                os.makedirs(os.path.join(project_full_path, "Assets"))
                os.makedirs(os.path.join(project_full_path, "Episodes"))
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create project: {e}")

# Example usage:
# if __name__ == "__main__":
#     import sys
#     from PySide2.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     dialog = CreateProjectDialog()
#     if dialog.exec_():
#         print("Project created")
#     else:
#         print("Cancelled")
#     sys.exit(app.exec_())
