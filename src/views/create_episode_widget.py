import os
import re
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

class CreateEpisodeDialog(QDialog):
    def __init__(self, project_code, parent=None):
        super(CreateEpisodeDialog, self).__init__(parent)
        
        self.project_code = project_code
        self.setWindowTitle("Create New Episode")
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Enter new episode number:")
        layout.addWidget(self.label)
        
        self.episode_name_input = QLineEdit()
        self.episode_name_input.textChanged.connect(self.sanity_check)
        layout.addWidget(self.episode_name_input)
        
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.create_episode)
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
        episode_name = self.episode_name_input.text()
        valid_pattern = re.compile(r'^\d{4}$')
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if valid_pattern.match(episode_name) and project_path:
            episode_path = os.path.join(project_path, self.project_code, "Episodes", episode_name)
            if not os.path.exists(episode_path):
                self.ok_button.setEnabled(True)
                return
        self.ok_button.setEnabled(False)

    def show_help(self):
        QMessageBox.information(self, "Episode Name Rules", "Episode number must be exactly 4 digits long and contain only numbers. The folder must not already exist.")
    
    def create_episode(self):
        episode_name = self.episode_name_input.text()
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if project_path:
            episode_path = os.path.join(project_path, self.project_code, "Episodes", episode_name)
            shots_path = os.path.join(episode_path, "shots")
            try:
                os.makedirs(shots_path)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create episode: {e}")

# Example usage:
# if __name__ == "__main__":
#     import sys
#     from PySide2.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     dialog = CreateEpisodeDialog("TEST")
#     if dialog.exec_():
#         print("Episode created")
#     else:
#         print("Cancelled")
#     sys.exit(app.exec_())
