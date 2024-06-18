# VFX Pipeline Manager

The VFX Pipeline Manager is a comprehensive tool designed to streamline the process of managing visual effects projects. It provides a user-friendly interface for creating and organizing projects, assets, episodes, and shots, with tailored support for different environments including Windows and Maya. 

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [File Structure](#file-structure)
5. [Environment Detection](#environment-detection)
6. [Components](#components)
7. [Extending the Manager](#extending-the-manager)
8. [Contributing](#contributing)
9. [License](#license)

## Features

- **Environment Detection**: Automatically detects and configures the environment (Windows, Linux, Maya).
- **Project Management**: Create and manage projects, episodes, shots, and assets.
- **Task Management**: Create and manage tasks and subtasks within projects.
- **Navigation Widgets**: Navigate through different assets and episodes.
- **Context Menus**: Custom context menus for tasks and outputs, supporting actions like open, import, and reference.
- **State Management**: Save and restore the state of the application.
- **Start Files**: Automatically copy start files for new tasks.

## Videos

### Video 1

<iframe src="https://drive.google.com/file/d/1EC8BnjJMon-vqy-UhLKk9sf_oukZzEbP](https://drive.google.com/file/d/16yly434CEmUWvp0JXX9e-J74VUeakTmo/preview"></iframe>

### Video 2


## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/BitBarn-Dev/Interum_FS_Manager.git
    cd Interum_FS_Manager
    ```

2. **Maya Integration**:
    To integrate the VFX Pipeline Manager with Maya, add the following script to your Maya Script Editor. Make sure to update the `script_path` variable to the location of your cloned repository.

    ```python
    import sys
    import maya.cmds as cmds

    # Add the script directory to Python path
    script_path = "C:/Users/srchr/Documents/PRTTM/FolderCreator/src"
    if script_path not in sys.path:
        sys.path.append(script_path)

    # Set the environment variable
    cmds.evalDeferred("import os; os.environ['PRTTM_DCC_ENV'] = 'maya'")

    # Run the script
    cmds.evalDeferred("import main; main.run_maya()")
    ```

    **Instructions for Running in Maya**:
    - Open Maya.
    - Open the Script Editor (you can find it under `Windows > General Editors > Script Editor`).
    - Copy and paste the script above into the Python tab of the Script Editor.
    - Update the `script_path` variable to the location where you cloned the repository.
    - Run the script by pressing the "Execute All" button (play icon).

    **Creating a Button for Quick Access**:
    - In the Script Editor, after pasting and updating the script, select the entire script.
    - Drag the selected script to the Maya shelf to create a new button.
    - Name the button appropriately (e.g., "VFX Pipeline Manager").
    - Now you can run the VFX Pipeline Manager directly by clicking this button on your Maya shelf.
    ```

## Usage

### Running the Application

- **Windows/Linux**:
    ```bash
    python src/main.py
    ```

- **Maya**:
    - Open Maya.
    - Open the Script Editor (you can find it under `Windows > General Editors > Script Editor`).
    - Copy and paste the script above into the Python tab of the Script Editor.
    - Update the `script_path` variable to the location where you cloned the repository.
    - Run the script by pressing the "Execute All" button (play icon).
    ```

### Creating Projects, Assets, Episodes, and Shots

1. **Create a New Project**:
    - Use the UI to enter a new project code (4 characters, uppercase letters, and numbers).
    
2. **Create a New Episode**:
    - Enter a new episode number (exactly 4 digits).

3. **Create a New Shot**:
    - Enter a sequence name (3 alphanumeric characters) and a shot number (3 digits).

4. **Create a New Asset**:
    - Enter a new asset name following the naming rules (camel case, starts with a lowercase letter, contains only letters and numbers).

## File Structure

```
VFXPipelineManager/
├── src/
│   ├── main.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── assets_nav_widget.py
│   │   ├── context_menus/
│   │   │   ├── __init__.py
│   │   │   ├── widgets_maya.py
│   │   │   ├── widgets_windows.py
│   │   ├── create_asset_widget.py
│   │   ├── create_episode_widget.py
│   │   ├── create_project_widget.py
│   │   ├── create_shot_widget.py
│   │   ├── main_menu_bar/
│   │   │   ├── __init__.py
│   │   │   ├── base_menu_bar.py
│   │   │   ├── menu_bar_maya.py
│   │   │   ├── menu_bar_windows.py
│   │   ├── navigation_widget.py
│   │   ├── outputs_tree_widget.py
│   │   ├── path_selector_widget.py
│   │   ├── tasks_tree_widget.py
│   │   ├── task_creator_widget.py
│   │   ├── publisher/
│   │   │   ├── __init__.py
│   │   │   ├── publisher_base.py
│   │   │   ├── publisher_maya.py
│   ├── utils/
│   │   ├── __init__.py
├── README.md
├── requirements.txt
```

## Environment Detection

The application detects the running environment and sets the `PRTTM_DCC_ENV` environment variable accordingly:
- **Linux**: Checks for `/etc/rocky-release` to detect Rocky Linux.
- **Windows**: Uses `sys.platform == 'win32'`.
- **Maya**: Checks if 'maya' is in `sys.modules`.

## Components

### Main Application (`main.py`)

- **VFXPipelineManager**: Main window class that initializes and manages the application's UI components.

### Views

- **NavigationWidget**: Manages navigation between projects, assets, and shots.
- **AssetsNavWidget**: Handles asset-specific navigation.
- **TasksTreeWidget**: Displays and manages tasks within the selected entity.
- **OutputsTreeWidget**: Displays and manages outputs within the selected entity.
- **PathSelectorWidget**: Allows users to select and update the projects path.
- **CreateProjectDialog**: Dialog for creating new projects.
- **CreateEpisodeDialog**: Dialog for creating new episodes.
- **CreateAssetDialog**: Dialog for creating new assets.
- **CreateShotDialog**: Dialog for creating new shots.
- **TaskCreatorWidget**: Dialog for creating new tasks.
- **Context Menus**: Custom context menus for tasks and outputs with environment-specific actions.

### Main Menu Bar

- **BaseMenuBar**: Base class for the menu bar.
- **WindowsMenuBar**: Menu bar for Windows environment.
- **MayaMenuBar**: Menu bar for Maya environment.

### Publisher

- **PublisherBase**: Base class for the publisher dialog.
- **PublisherMaya**: Publisher dialog specific to Maya, including sanity checks and publishing tasks.

## Extending the Manager

To extend the VFX Pipeline Manager, you can add new widgets, dialogs, or modify the existing ones. Ensure you follow the existing structure and naming conventions to maintain consistency.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate documentation and tests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
