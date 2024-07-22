import os
from PySide2.QtWidgets import QMenu, QMessageBox
from maya import cmds

class TaskTreeContext:
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget

    def create_context_menu(self, item, position):
        menu = QMenu(self.parent_widget)
        open_action = menu.addAction("Open")
        open_folder_action = menu.addAction("Open Folder")
        action = menu.exec_(position)
        self.handle_action(action, open_action, open_folder_action, item)
    
    def handle_action(self, action, open_action, open_folder_action, item):
        if action == open_action:
            self.open_item(item)
        elif action == open_folder_action:
            self.open_item_folder(item)

    def open_item(self, item):
        path = self.build_path_from_item(item)
        if os.path.isfile(path):
            if path.endswith('.ma') or path.endswith('.mb'):
                self.prompt_save_if_needed(path)
            else:
                os.startfile(path)
        elif os.path.isdir(path):
            os.startfile(path)

    def prompt_save_if_needed(self, path):
        if cmds.file(query=True, modified=True):
            result = cmds.confirmDialog(
                title='Unsaved Changes',
                message='Your current scene has unsaved changes. What would you like to do?',
                button=['Save', 'Discard', 'Cancel'],
                defaultButton='Save',
                cancelButton='Cancel',
                dismissString='Cancel'
            )
            if result == 'Save':
                if cmds.file(save=True):
                    self.load_file_in_maya(path)
            elif result == 'Discard':
                self.load_file_in_maya(path)
            # 'Cancel' does nothing
        else:
            self.load_file_in_maya(path)

    def load_file_in_maya(self, path):
        cmds.file(path, open=True, force=True)

    def open_item_folder(self, item):
        path = self.build_path_from_item(item)
        os.startfile(os.path.dirname(path))

    def build_path_from_item(self, item):
        parts = []
        while item:
            parts.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.parent_widget.entity_path, 'tasks', *parts)

class OutputTreeContext(TaskTreeContext):
    def __init__(self, parent_widget):
        super(OutputTreeContext, self).__init__(parent_widget)

    def create_context_menu(self, item, position):
        menu = QMenu(self.parent_widget)
        import_action = menu.addAction("Import")
        reference_action = menu.addAction("Reference")
        open_folder_action = menu.addAction("Open Folder")
        action = menu.exec_(position)
        self.handle_action(action, open_folder_action, import_action, reference_action, item)

    def handle_action(self, action, open_folder_action, import_action, reference_action, item):
        if action == open_folder_action:
            self.open_item_folder(item)
        elif action == import_action:
            self.import_item(item)
        elif action == reference_action:
            self.reference_item(item)

    def import_item(self, item):
        path = self.build_path_from_item(item)
        if os.path.isfile(path) and (path.endswith('.ma') or path.endswith('.mb')):
            cmds.file(path, i=True)
        else:
            QMessageBox.warning(self.parent_widget, "Import Error", "Selected item is not a valid Maya file.")

    def reference_item(self, item):
        path = self.build_path_from_item(item)
        if os.path.isfile(path) and (path.endswith('.ma') or path.endswith('.mb') or path.endswith('.abc')):
            # Extract the basename without extension to use as namespace
            namespace = os.path.splitext(os.path.basename(path))[0]
            if path.endswith('.abc'):
                cmds.file(path, reference=True, type="Alembic", namespace=namespace)
            else:
                cmds.file(path, reference=True, namespace=namespace)
        else:
            QMessageBox.warning(self.parent_widget, "Reference Error", "Selected item is not a valid Maya or Alembic file.")

    def build_path_from_item(self, item):
        parts = []
        while item:
            parts.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.parent_widget.entity_path, 'outputs', *parts)
