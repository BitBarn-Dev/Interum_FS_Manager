import os
import re
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

class CreateAssetDialog(QDialog):
    def __init__(self, project_code, asset_type, parent=None):
        super(CreateAssetDialog, self).__init__(parent)
        
        self.project_code = project_code
        self.asset_type = asset_type
        self.setWindowTitle("Create New Asset")
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Enter new asset name:")
        layout.addWidget(self.label)
        
        self.asset_name_input = QLineEdit()
        self.asset_name_input.textChanged.connect(self.sanity_check)
        layout.addWidget(self.asset_name_input)
        
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.create_asset)
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
        asset_name = self.asset_name_input.text()
        valid_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if valid_pattern.match(asset_name) and project_path:
            asset_path = os.path.join(project_path, self.project_code, "Assets", self.asset_type, asset_name)
            if not os.path.exists(asset_path):
                self.ok_button.setEnabled(True)
                return
        self.ok_button.setEnabled(False)

    def show_help(self):
        QMessageBox.information(self, "Asset Name Rules", "Asset name must be in camel case, start with a lower case letter, and contain only letters and numbers. No spaces or special characters are allowed.")
    
    def create_asset(self):
        asset_name = self.asset_name_input.text()
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if project_path:
            asset_path = os.path.join(project_path, self.project_code, "Assets", self.asset_type, asset_name)
            try:
                os.makedirs(os.path.join(asset_path, "tasks"))
                os.makedirs(os.path.join(asset_path, "outputs"))
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create asset: {e}")

# Example usage:
# if __name__ == "__main__":
#     import sys
#     from PySide2.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     dialog = CreateAssetDialog("TEST", "CHR")
#     if dialog.exec_():
#         print("Asset created")
#     else:
#         print("Cancelled")
#     sys.exit(app.exec_())
