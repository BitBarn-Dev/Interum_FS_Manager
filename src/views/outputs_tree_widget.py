import os
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import Qt
from views.context_menus import OutputTreeContext

class OutputsTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(OutputsTreeWidget, self).__init__(parent)
        self.setHeaderLabels(["Outputs"])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.current_state = None  # Add this to store the current state
        self.entity_path = None  # Add this to store the entity path
        self.context_menu = OutputTreeContext(self)  # Initialize the context menu handler

    def update_entity(self, entity_path=None, current_state=None, expanded_items=None):
        self.current_state = current_state  # Set the current state
        self.entity_path = entity_path  # Set the entity path
        self.clear()
        if entity_path:
            outputs_path = os.path.join(entity_path, 'outputs')
            if os.path.exists(outputs_path):
                print(f"Updating Outputs Tree with outputs path: {outputs_path}")
                self.build_tree_from_path(outputs_path)
                # Restore the expanded state
                self.restore_expanded_items(expanded_items)
        else:
            print("No entity selected. Clearing Outputs Tree.")

    def get_expanded_items(self):
        expanded_items = []
        root = self.invisibleRootItem()
        stack = [root]
        while stack:
            item = stack.pop()
            if item.isExpanded():
                expanded_items.append(self.build_path_from_item(item))
            for i in range(item.childCount()):
                stack.append(item.child(i))
        return expanded_items

    def restore_expanded_items(self, expanded_items):
        if expanded_items is None:
            return
        root = self.invisibleRootItem()
        stack = [root]
        while stack:
            item = stack.pop()
            item_path = self.build_path_from_item(item)
            if item_path in expanded_items:
                item.setExpanded(True)
            for i in range(item.childCount()):
                stack.append(item.child(i))

    def build_tree_from_path(self, path):
        root_item = self.invisibleRootItem()
        path_map = {path: root_item}

        for root, dirs, files in os.walk(path):
            parent_item = path_map[root]
            for folder in sorted(dirs):
                folder_path = os.path.join(root, folder)
                folder_item = QTreeWidgetItem([folder])
                parent_item.addChild(folder_item)
                path_map[folder_path] = folder_item

            for file in sorted(files):
                file_item = QTreeWidgetItem([file])
                parent_item.addChild(file_item)

    def build_path_from_item(self, item):
        parts = []
        while item:
            parts.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.entity_path, 'outputs', *parts)

    def open_context_menu(self, position):
        item = self.itemAt(position)
        if item:
            self.context_menu.create_context_menu(item, self.viewport().mapToGlobal(position))
