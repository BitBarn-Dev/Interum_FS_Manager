import os
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMessageBox

class CreateAssetTypeDialog(QDialog):
    def __init__(self, project_code, parent=None):
        super(CreateAssetTypeDialog, self).__init__(parent)
        
        self.project_code = project_code
        self.setWindowTitle("Create New Asset Type")
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Select new asset type:")
        layout.addWidget(self.label)
        
        self.asset_type_dropdown = QComboBox()
        self.asset_type_dropdown.addItem("<select one>")
        self.asset_types = {
            "CHR": "Characters (Characters)",
            "PRP": "Props (Props)",
            "ENV": "Environments (Environments)",
            "BLD": "Buildings (Buildings)",
            "CLTH": "Clothing/Cloth (Clothing/Cloth)",
            "MCP": "Motion Capture (Motion Capture)",
            "ANIM": "Animation (Animation)",
            "VEH": "Vehicles (Vehicles)",
            "LUT": "Show Luts (Show Luts)"
        }
        for key, value in self.asset_types.items():
            self.asset_type_dropdown.addItem(f"{key}: {value}")
        self.asset_type_dropdown.currentIndexChanged.connect(self.sanity_check)
        layout.addWidget(self.asset_type_dropdown)
        
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.create_asset_type)
        self.ok_button.setEnabled(False)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def sanity_check(self):
        selected_text = self.asset_type_dropdown.currentText()
        asset_type_code = selected_text.split(":")[0]
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if asset_type_code in self.asset_types and project_path:
            asset_type_path = os.path.join(project_path, self.project_code, "Assets", asset_type_code)
            if not os.path.exists(asset_type_path):
                self.ok_button.setEnabled(True)
                return
        self.ok_button.setEnabled(False)

    def create_asset_type(self):
        selected_text = self.asset_type_dropdown.currentText()
        asset_type_code = selected_text.split(":")[0]
        project_path = os.getenv('PRTTM_PROJECTS_PATH')
        
        if project_path:
            asset_type_path = os.path.join(project_path, self.project_code, "Assets", asset_type_code)
            try:
                os.makedirs(asset_type_path)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create asset type: {e}")

# Example usage:
# if __name__ == "__main__":
#     import sys
#     from PySide2.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     dialog = CreateAssetTypeDialog("TEST")
#     if dialog.exec_():
#         print("Asset type created")
#     else:
#         print("Cancelled")
#     sys.exit(app.exec_())
