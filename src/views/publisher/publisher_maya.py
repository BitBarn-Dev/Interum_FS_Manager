from PySide2.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide2.QtCore import Qt
import os
import re
import shutil
from maya import cmds

class PublisherMaya(QDialog):
    def __init__(self, file_path, parent=None):
        super(PublisherMaya, self).__init__(parent)
        self.setWindowTitle("Maya Publisher")
        self.setMinimumWidth(500)

        self.file_path = file_path
        self.basename = os.path.basename(file_path).rsplit('.', 1)[0]

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.filename_label = QLabel(f"Publishing: {self.basename}", self)
        self.layout.addWidget(self.filename_label)

        self.sanity_check_button = QPushButton("Run Sanity Check", self)
        self.sanity_check_button.clicked.connect(self.show_sanity_check_results)
        self.layout.addWidget(self.sanity_check_button)

        self.publish_button = QPushButton("Publish", self)
        self.publish_button.clicked.connect(self.publish)
        self.layout.addWidget(self.publish_button)

    def show_sanity_check_results(self):
        check_result, messages = self.run_sanity_check()
        if check_result == 'pass':
            QMessageBox.information(self, "Sanity Check", "Sanity check passed.")
        else:
            self.display_sanity_check_messages(check_result, messages)

    def run_sanity_check(self):
        messages = []
        task_code = self.get_task_code(self.file_path)
        output_path = self.get_output_path(self.file_path, task_code)

        if os.path.exists(output_path):
            messages.append({"type": "error", "message": f"Output file {output_path} already exists."})

        if messages:
            if any(msg["type"] == "error" for msg in messages):
                return 'fail', messages
            return 'warning', messages

        return 'pass', messages

    def display_sanity_check_messages(self, check_result, messages):
        dialog = QDialog(self)
        dialog.setWindowTitle("Sanity Check Results")
        dialog.setMinimumWidth(500)
        layout = QVBoxLayout(dialog)

        table = QTableWidget(len(messages), 2, dialog)
        table.setHorizontalHeaderLabels(["Type", "Message"])
        for row, msg in enumerate(messages):
            table.setItem(row, 0, QTableWidgetItem(msg["type"]))
            table.setItem(row, 1, QTableWidgetItem(msg["message"]))
        layout.addWidget(table)

        button_layout = QHBoxLayout()
        if check_result == 'warning':
            continue_button = QPushButton("Continue Anyway", dialog)
            continue_button.clicked.connect(lambda: dialog.done(1))
            button_layout.addWidget(continue_button)

        ok_button = QPushButton("OK", dialog)
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        return dialog.exec_()

    def publish(self):
        check_result, messages = self.run_sanity_check()
        if check_result == 'fail':
            self.display_sanity_check_messages(check_result, messages)
            QMessageBox.warning(self, "Sanity Check Failed", "Sanity check failed. Please fix the issues and try again.")
            return
        elif check_result == 'warning':
            result = self.display_sanity_check_messages(check_result, messages)
            if result != 1:
                return

        task_code = self.get_task_code(self.file_path)
        output_path = self.get_output_path(self.file_path, task_code)
        try:
            cmds.file(rename=output_path)
            cmds.file(save=True, type='mayaAscii')
            self.iterate_and_open_file()
            QMessageBox.information(self, "Publish Successful", f"File has been successfully published to {output_path}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Publish Failed", f"An error occurred during publish: {str(e)}")

    def get_task_code(self, file_path):
        basename = os.path.basename(file_path).rsplit('.', 1)[0]
        if "Assets" in file_path:
            return basename.split('_')[3]
        elif "Episodes" in file_path:
            return basename.split('_')[4]
        return None

    def get_output_path(self, file_path, task_code):
        base_path, _ = file_path.split("tasks", 1)
        output_dir = os.path.join(base_path, "outputs", task_code, self.basename)
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, os.path.basename(file_path))

    def iterate_and_open_file(self):
        dir_name, file_name = os.path.split(self.file_path)
        match = re.match(r'(.+_v)(\d+)(\.\w+)', file_name)
        if match:
            prefix, version, suffix = match.groups()
            new_version = int(version) + 1
            new_file_name = f"{prefix}{new_version:03d}{suffix}"
        else:
            base_name, ext = os.path.splitext(file_name)
            new_file_name = f"{base_name}_v001{ext}"

        new_file_path = os.path.join(dir_name, new_file_name)
        shutil.copy(self.file_path, new_file_path)
        cmds.file(new_file_path, open=True, force=True)
