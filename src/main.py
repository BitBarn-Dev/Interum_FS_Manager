import os
import sys

# Set the environment variable if not already set
if 'PRTTM_DCC_ENV' not in os.environ:
    if sys.platform == 'linux' and os.path.exists('/etc/rocky-release'):
        os.environ['PRTTM_DCC_ENV'] = 'rocky'
    elif sys.platform == 'win32':
        os.environ['PRTTM_DCC_ENV'] = 'windows'
    elif 'maya' in sys.modules:
        os.environ['PRTTM_DCC_ENV'] = 'maya'
    else:
        os.environ['PRTTM_DCC_ENV'] = 'unknown'

import json
import shutil
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PySide2 import QtCore
# Import your views
from views.path_selector_widget import PathSelectorWidget
from views.navigation_widget import NavigationWidget
from views.tasks_tree_widget import TasksTreeWidget
from views.outputs_tree_widget import OutputsTreeWidget
from views.main_menu_bar import MainMenuBar  # Import the menu bar

class VFXPipelineManager(QWidget):
    def __init__(self, parent=None):
        super(VFXPipelineManager, self).__init__(parent)
        
        self.setWindowTitle('VFX Pipeline Manager')
        self.setGeometry(300, 300, 800, 600)
        
        self.layout = QVBoxLayout()
        
        self.menu_bar = MainMenuBar(self)
        self.layout.setMenuBar(self.menu_bar)
        
        self.path_selector = PathSelectorWidget(self)
        self.layout.addWidget(self.path_selector)
        
        self.navigation_widget = NavigationWidget(self)
        self.layout.addWidget(self.navigation_widget)
        
        self.tabs = QTabWidget()
        
        self.tasks_tree = TasksTreeWidget()
        self.outputs_tree = OutputsTreeWidget()
        
        self.tabs.addTab(self.tasks_tree, "Tasks")
        self.tabs.addTab(self.outputs_tree, "Outputs")
        
        self.layout.addWidget(self.tabs)
        
        self.setLayout(self.layout)
        
        # Connect the path_updated signal to the navigation widget's update method
        self.path_selector.path_updated.connect(self.update_project_path)
        
        # Connect the navigation_updated signal to the update_entities method
        self.navigation_widget.navigation_updated.connect(self.update_entities)
        
        # Connect the files_updated signal to the update_entities method
        self.menu_bar.files_updated.connect(self.update_entities)
        
        # Load initial state
        self.load_initial_state()

        # Ensure start_files.json and start_files folder exist
        self.ensure_start_files()

    def load_initial_state(self):
        state = self.load_state()
        projects_path = state.get('projects_path', None)
        if projects_path:
            self.path_selector.set_path(projects_path)

    def load_state(self):
        state_file = self.get_state_file_path()
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                return json.load(f)
        return {}

    def save_state(self, state):
        state_file = self.get_state_file_path()
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=4)

    def get_state_file_path(self):
        home_dir = os.path.expanduser("~")
        state_dir = os.path.join(home_dir, '.prttm', 'tools', 'fs_manager')
        os.makedirs(state_dir, exist_ok=True)
        return os.path.join(state_dir, 'state.json')

    def ensure_start_files(self):
        state_file = self.get_state_file_path()
        start_files_json_path = os.path.join(os.path.dirname(state_file), 'start_files.json')
        start_files_dir_path = os.path.join(os.path.dirname(state_file), 'start_files')

        if not os.path.exists(start_files_json_path):
            template_json_path = os.path.join(os.path.dirname(__file__), 'resources', 'start_files.json')
            shutil.copy(template_json_path, start_files_json_path)
        
        if not os.path.exists(start_files_dir_path):
            template_dir_path = os.path.join(os.path.dirname(__file__), 'resources', 'start_files')
            shutil.copytree(template_dir_path, start_files_dir_path)

    def update_project_path(self, path):
        os.environ['PRTTM_PROJECTS_PATH'] = path
        self.navigation_widget.update_project_path()
        self.update_state(path)

    def update_state(self, path):
        state = self.load_state()
        state['projects_path'] = path
        self.save_state(state)
    
    def update_entities(self):
        current_state = self.navigation_widget.get_current_state()
        if self.navigation_widget.is_entity_selected():
            entity_path = self.navigation_widget.get_current_path()
        else:
            entity_path = None

        expanded_tasks = self.tasks_tree.get_expanded_items()
        expanded_outputs = self.outputs_tree.get_expanded_items()

        self.tasks_tree.update_entity(entity_path=entity_path, current_state=current_state, expanded_items=expanded_tasks)
        self.outputs_tree.update_entity(entity_path=entity_path, current_state=current_state, expanded_items=expanded_outputs)

def run_app():
    app = QApplication(sys.argv)
    main_win = VFXPipelineManager()
    main_win.show()
    sys.exit(app.exec_())

def run_maya():
    from maya import cmds
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance
    from PySide2 import QtWidgets

    def get_maya_main_window():
        """
        Get the Maya main window as a QtWidgets.QWidget.
        """
        maya_main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    # Create the application window
    maya_main_window = get_maya_main_window()
    main_win = VFXPipelineManager(parent=maya_main_window)
    main_win.setWindowFlags(main_win.windowFlags() | QtCore.Qt.Window)
    main_win.show()

    return main_win

if __name__ == "__main__":
    if os.environ['PRTTM_DCC_ENV'] == 'maya':
        run_maya()
    else:
        run_app()
