from PySide2.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel, QGroupBox, QMessageBox, QListWidget
from PySide2.QtCore import Signal
import os
import re
import json
import shutil

class TaskCreatorWidget(QDialog):
    task_created = Signal(str)  # Signal to emit the new task code

    def __init__(self, entity_path, navigation_state, parent=None):
        super(TaskCreatorWidget, self).__init__(parent)
        
        self.setWindowTitle("Task Creator")
        self.entity_path = entity_path
        self.navigation_state = navigation_state
        
        self.layout = QVBoxLayout()
        
        # Task code dropdown
        self.task_code_label = QLabel("Task Code:")
        self.layout.addWidget(self.task_code_label)
        
        self.task_code_dropdown = QComboBox()
        self.task_code_dropdown.addItems(self.get_task_codes())
        self.task_code_dropdown.currentTextChanged.connect(self.update_task_code)
        self.layout.addWidget(self.task_code_dropdown)
        
        # Subtask input
        self.subtask_label = QLabel("Subtask (Optional):")
        self.layout.addWidget(self.subtask_label)
        
        self.subtask_edit = QLineEdit()
        self.subtask_edit.setPlaceholderText("Optional")
        self.subtask_edit.textChanged.connect(self.update_task_code)
        self.layout.addWidget(self.subtask_edit)
        
        # Task code display
        self.task_code_display = QLabel("")
        self.layout.addWidget(self.task_code_display)
        
        # Help button
        help_button = QPushButton("?")
        help_button.setFixedSize(20, 20)
        help_button.clicked.connect(self.show_help)
        self.layout.addWidget(help_button)
        
        # Start files group box
        self.start_files_groupbox = QGroupBox("Start Files")
        self.start_files_layout = QVBoxLayout()
        self.start_files_list = QListWidget()
        self.start_files_layout.addWidget(self.start_files_list)
        self.start_files_groupbox.setLayout(self.start_files_layout)
        self.layout.addWidget(self.start_files_groupbox)
        
        # Create button
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_task)
        self.create_button.setEnabled(False)
        self.layout.addWidget(self.create_button)
        
        self.setLayout(self.layout)
        
        # Load and display start files
        self.update_task_code()

    def get_task_codes(self):
        start_file_map = self.load_start_file_map()
        task_codes = []
        for category in start_file_map.values():
            if isinstance(category, dict):
                task_codes.extend(category.keys())
        return sorted(set(task_codes))
    
    def load_start_file_map(self):
        home_dir = os.path.expanduser("~")
        start_files_path = os.path.join(home_dir, '.prttm', 'tools', 'fs_manager', 'start_files.json')
        if os.path.exists(start_files_path):
            with open(start_files_path, 'r') as f:
                return json.load(f)
        return {}

    def update_task_code(self):
        task_code = self.task_code_dropdown.currentText()
        subtask = self.subtask_edit.text()
        full_task_code = self.generate_task_code(task_code, subtask)
        self.task_code_display.setText(full_task_code)
        
        # Validate task code
        if re.match(r'^[a-zA-Z0-9]+$', full_task_code):
            self.create_button.setEnabled(True)
            self.update_start_files_list(task_code)
        else:
            self.create_button.setEnabled(False)
            self.start_files_list.clear()

    def generate_task_code(self, task_code, subtask):
        if subtask:
            return re.sub(r'\W+', '', f"{task_code}{subtask.capitalize()}")
        else:
            return re.sub(r'\W+', '', task_code)
    
    def show_help(self):
        QMessageBox.information(self, "Naming Rules", "Task codes and subtasks must be alphanumeric and can only contain letters and digits. Special characters are not allowed.")
    
    def update_start_files_list(self, task_code):
        self.start_files_list.clear()
        task_type = self.get_task_type(task_code)
        start_files_path = self.get_default_file_path(task_type)
        
        start_file_map = self.load_start_file_map()
        
        files_to_copy = []
        if task_code in start_file_map.get(task_type, {}):
            task_files = start_file_map[task_type][task_code]
            if task_files is None:
                files_to_copy = [f for f in os.listdir(start_files_path) if f.startswith('default.')]
            else:
                files_to_copy = task_files
        
        for file in files_to_copy:
            destination_file = self.get_destination_filename(task_code, file, self.subtask_edit.text())
            self.start_files_list.addItem(destination_file)

    def get_task_type(self, task_code):
        start_file_map = self.load_start_file_map()
        if task_code in start_file_map.get('2D', {}):
            return '2D'
        elif task_code in start_file_map.get('3D', {}):
            return '3D'
        return None

    def get_default_file_path(self, task_type):
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, '.prttm', 'tools', 'fs_manager', 'start_files', task_type)
    
    def get_destination_filename(self, task_code, file, subtask):
        extension = file.split('.')[-1]
        full_task_code = self.generate_task_code(task_code, subtask)
        if self.navigation_state.get('shot'):
            return f"{self.navigation_state['project_code']}_{self.navigation_state['episode']}_{self.navigation_state['shot']}_{full_task_code}_v001.{extension}"
        elif self.navigation_state.get('asset'):
            return f"{self.navigation_state['project_code']}_{self.navigation_state['asset_type']}_{self.navigation_state['asset']}_{full_task_code}_v001.{extension}"
        return file

    def create_sandbox_structure(self, base_directory):
        """
        Create the _sandbox folder and its subfolders within the given base_directory.
        
        Args:
            base_directory (str): The path to the base directory where the _sandbox folder should be created.
        """
        subfolders = [
            'ma',
            'mb',
            'fbx',
            'obj',
            'abc',
            'hou',
            'hda',
            'psd',
            '_caches',
            '_staging'
        ]
        
        sandbox_dir = os.path.join(base_directory, '_sandbox')
        
        os.makedirs(sandbox_dir, exist_ok=True)
        
        for subfolder in subfolders:
            subfolder_path = os.path.join(sandbox_dir, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)

    def create_task(self):
        task_code = self.task_code_dropdown.currentText()
        subtask = self.subtask_edit.text()
        full_task_code = self.generate_task_code(task_code, subtask)
        print(f"Creating task: {full_task_code}, Subtask: {subtask}")

        task_folder = os.path.join(self.entity_path, 'tasks', full_task_code)
        
        # Check if the task folder already exists
        if os.path.exists(task_folder):
            QMessageBox.warning(self, "Task Exists", f"The task folder '{task_folder}' already exists.")
            return
        
        task_type = self.get_task_type(task_code)
        start_files_path = self.get_default_file_path(task_type)
        
        start_file_map = self.load_start_file_map()
        
        files_to_copy = []
        if task_code in start_file_map.get(task_type, {}):
            task_files = start_file_map[task_type][task_code]
            if task_files is None:
                files_to_copy = [f for f in os.listdir(start_files_path) if f.startswith('default.')]
            else:
                files_to_copy = task_files

        os.makedirs(task_folder, exist_ok=True)
        
        # Create the _sandbox structure
        self.create_sandbox_structure(task_folder)

        for file in files_to_copy:
            src = os.path.join(start_files_path, file)
            dst = os.path.join(task_folder, self.get_destination_filename(task_code, file, subtask))
            print(f"Copying {src} to {dst}")
            shutil.copy(src, dst)

        self.task_created.emit(full_task_code)  # Emit the signal with the new task code
        self.accept()
