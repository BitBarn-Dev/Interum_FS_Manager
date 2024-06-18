from PySide2.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox, QFileDialog, QHBoxLayout
from PySide2.QtCore import Qt
import os
import re
from views.navigation_widget import NavigationWidget

class SaveAsDialog(QDialog):
    def __init__(self, file_extension=".ma", parent=None):
        super(SaveAsDialog, self).__init__(parent)
        self.setWindowTitle("Save As")
        self.file_extension = file_extension
        self.selected_file = None

        self.layout = QVBoxLayout(self)

        # Help button
        help_button = QPushButton("?")
        help_button.setFixedSize(20, 20)
        help_button.clicked.connect(self.show_help)
        help_layout = QHBoxLayout()
        help_layout.addStretch()
        help_layout.addWidget(help_button)
        self.layout.addLayout(help_layout)
        
        # Navigation Widget
        self.navigation_widget = NavigationWidget(self)
        self.navigation_widget.navigation_updated.connect(self.update_tasks_list)
        self.layout.addWidget(self.navigation_widget)
        
        # Tasks List
        self.tasks_list = QListWidget(self)
        self.tasks_list.currentTextChanged.connect(self.update_filename_preview)
        self.layout.addWidget(self.tasks_list)
        
        # Filename Preview Label
        self.filename_preview_label = QLabel("Filename Preview: ", self)
        self.layout.addWidget(self.filename_preview_label)
        
        # Save to Task Button
        self.save_button = QPushButton("Save to Task", self)
        self.save_button.clicked.connect(self.save_to_task)
        self.layout.addWidget(self.save_button)

        # Save Manually Button
        self.save_manually_button = QPushButton("Save Manually", self)
        self.save_manually_button.clicked.connect(self.save_manually)
        self.layout.addWidget(self.save_manually_button)

    def update_tasks_list(self):
        self.tasks_list.clear()
        current_state = self.navigation_widget.get_current_state()
        entity_path = self.navigation_widget.get_current_path()
        
        if entity_path:
            tasks_path = os.path.join(entity_path, 'tasks')
            if os.path.exists(tasks_path):
                for task in sorted(os.listdir(tasks_path)):
                    task_path = os.path.join(tasks_path, task)
                    if os.path.isdir(task_path):
                        self.tasks_list.addItem(task)

    def update_filename_preview(self, task_name):
        current_state = self.navigation_widget.get_current_state()
        entity_path = self.navigation_widget.get_current_path()
        
        if entity_path and task_name:
            task_path = os.path.join(entity_path, 'tasks', task_name)
            latest_version = self.get_latest_version(task_path)
            if latest_version:
                new_version = f"v{int(latest_version[1:]) + 1:03d}"
            else:
                new_version = "v001"
            
            filename = self.get_destination_filename(current_state, task_name, new_version, self.file_extension)
            self.filename_preview_label.setText(f"Filename Preview: {filename}")

    def get_latest_version(self, task_path):
        version_pattern = re.compile(r'_v(\d+)\.')
        latest_version = None
        
        for file in os.listdir(task_path):
            match = version_pattern.search(file)
            if match:
                version = match.group(1)
                if not latest_version or int(version) > int(latest_version[1:]):
                    latest_version = f"v{version}"
        
        return latest_version

    def get_destination_filename(self, current_state, task_code, version, extension):
        if current_state.get('shot'):
            return f"{current_state['project_code']}_{current_state['episode']}_{current_state['shot']}_{task_code}_{version}{extension}"
        elif current_state.get('asset'):
            return f"{current_state['project_code']}_{current_state['asset_type']}_{current_state['asset']}_{task_code}_{version}{extension}"
        return f"{task_code}_{version}{extension}"

    def save_to_task(self):
        current_state = self.navigation_widget.get_current_state()
        task_name = self.tasks_list.currentItem().text()
        entity_path = self.navigation_widget.get_current_path()
        
        if entity_path and task_name:
            task_path = os.path.join(entity_path, 'tasks', task_name)
            latest_version = self.get_latest_version(task_path)
            if latest_version:
                new_version = f"v{int(latest_version[1:]) + 1:03d}"
            else:
                new_version = "v001"
            
            filename = self.get_destination_filename(current_state, task_name, new_version, self.file_extension)
            self.selected_file = os.path.join(task_path, filename)
            self.filename_preview_label.setText(f"Selected File: {self.selected_file}")
            self.accept()
        else:
            QMessageBox.warning(self, "Save to Task", "Please select a task to save to.")

    def save_manually(self):
        reply = QMessageBox.warning(self, "Save Manually", "The preferred method is to save to a task. Do you want to continue with manual save?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            file_dialog = QFileDialog(self, "Save As", filter=f"*{self.file_extension}")
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            if file_dialog.exec_():
                self.selected_file = file_dialog.selectedFiles()[0]
                self.filename_preview_label.setText(f"Selected File: {self.selected_file}")
                self.accept()

    def show_help(self):
        QMessageBox.information(self, "Help", "This tool allows you to save files to a task with versioning.\n\n"
                                              "1. Select a task from the list.\n"
                                              "2. The filename preview will show the next version number.\n"
                                              "3. Click 'Save to Task' to save the file with the new version.\n"
                                              "4. Click 'Save Manually' to manually select a location and name for the file, though this is not the preferred method.")

    def get_selected_file(self):
        return self.selected_file
