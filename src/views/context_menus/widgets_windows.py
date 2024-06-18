# views/context_menus/utils_windows.py

import os
from PySide2.QtWidgets import QMenu

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
            os.startfile(path)
        elif os.path.isdir(path):
            os.startfile(path)

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

    def build_path_from_item(self, item):
        parts = []
        while item:
            parts.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.parent_widget.entity_path, 'outputs', *parts)        


