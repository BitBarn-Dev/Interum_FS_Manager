# views/tasks_tree_widget.py

import os
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QDialog
from PySide2.QtCore import Qt
from views.task_creator_widget import TaskCreatorWidget
from views.context_menus import TaskTreeContext

class TasksTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(TasksTreeWidget, self).__init__(parent)
        self.setHeaderLabels(["Tasks"])
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.current_state = None  # Add this to store the current state
        self.entity_path = None  # Add this to store the entity path
        self.context_menu = TaskTreeContext(self)  # Initialize the context menu handler

    def update_entity(self, entity_path=None, current_state=None, expanded_items=None):
        self.current_state = current_state  # Set the current state
        self.entity_path = entity_path  # Set the entity path
        self.clear()
        if entity_path:
            tasks_path = os.path.join(entity_path, 'tasks')
            if os.path.exists(tasks_path):
                print(f"Updating Tasks Tree with tasks path: {tasks_path}")
                self.build_tree_from_path(tasks_path)
                # Add the "Create New" item at the top level
                create_new_item = QTreeWidgetItem(["Create New"])
                self.addTopLevelItem(create_new_item)
                # Restore the expanded state
                self.restore_expanded_items(expanded_items)
        else:
            print("No entity selected. Clearing Tasks Tree.")


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
        return os.path.join(self.entity_path, 'tasks', *parts)                

    def on_item_double_clicked(self, item, column):
        if item.text(0) == "Create New":
            self.open_task_creator_dialog()
        else:
            self.open_item(item)

    def open_task_creator_dialog(self):
        dialog = TaskCreatorWidget(self.entity_path, self.current_state, self)
        dialog.task_created.connect(self.on_task_created)  # Connect the signal to the handler
        if dialog.exec_() == QDialog.Accepted:
            # Handle the result from the dialog if needed
            print("Task created")

    def on_task_created(self, task_code):
        # Refresh the tree
        self.update_entity(self.entity_path, self.current_state)
        # Expand and select the newly created item
        self.expand_and_select_task(task_code)

    def expand_and_select_task(self, task_code):
        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            if item.text(0) == task_code:
                self.setCurrentItem(item)
                item.setExpanded(True)
                break

    def open_context_menu(self, position):
        item = self.itemAt(position)
        if item:
            self.context_menu.create_context_menu(item, self.viewport().mapToGlobal(position))
