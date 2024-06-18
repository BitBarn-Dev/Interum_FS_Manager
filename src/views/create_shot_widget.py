import os
import re
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

class CreateShotDialog(QDialog):
    def __init__(self, project_code, episode_code, parent=None):
        super(CreateShotDialog, self).__init__(parent)
        
        self.project_code = project_code
        self.episode_code = episode_code
        self.setWindowTitle("Create New Shot")
        
        layout = QVBoxLayout()
        
        self.sequence_label = QLabel("Enter sequence name (3 alphanumeric characters):")
        layout.addWidget(self.sequence_label)
        
        self.sequence_input = QLineEdit()
        self.sequence_input.textChanged.connect(self.sanity_check)
        layout.addWidget(self.sequence_input)
        
        self.shot_label = QLabel("Enter shot number (3 digits):")
        layout.addWidget(self.shot_label)
        
        self.shot_input = QLineEdit()
        self.shot_input.textChanged.connect(self.sanity_check)
        layout.addWidget(self.shot_input)
        
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.create_shot)
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
        sequence_name = self.sequence_input.text()
        shot_name = self.shot_input.text()
        valid_sequence_pattern = re.compile(r'^[a-zA-Z0-9]{3}$')
        valid_shot_pattern = re.compile(r'^\d{3}$')
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if valid_sequence_pattern.match(sequence_name) and valid_shot_pattern.match(shot_name) and project_path:
            shot_full_name = f"{sequence_name}_{shot_name}"
            shot_path = os.path.join(project_path, self.project_code, "Episodes", self.episode_code, "shots", shot_full_name)
            if not os.path.exists(shot_path):
                self.ok_button.setEnabled(True)
                return
        self.ok_button.setEnabled(False)

    def show_help(self):
        QMessageBox.information(self, "Shot Name Rules", "Sequence name must be 3 alphanumeric characters.\nShot number must be 3 digits.\nThe combined shot name must be unique.")

    def create_shot(self):
        sequence_name = self.sequence_input.text()
        shot_name = self.shot_input.text()
        shot_full_name = f"{sequence_name}_{shot_name}"
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if project_path:
            shot_path = os.path.join(project_path, self.project_code, "Episodes", self.episode_code, "shots", shot_full_name)
            try:
                os.makedirs(shot_path)
                os.makedirs(os.path.join(shot_path, "tasks"))
                os.makedirs(os.path.join(shot_path, "outputs"))
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create shot: {e}")

# Example usage:
# if __name__ == "__main__":
#     import sys
#     from PySide2.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     dialog = CreateShotDialog("TEST", "0001")
#     if dialog.exec_():
#         print("Shot created")
#     else:
#         print("Cancelled")
#     sys.exit(app.exec_())
