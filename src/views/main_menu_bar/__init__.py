# views/main_menu_bar/__init__.py

import os

env = os.environ.get('PRTTM_DCC_ENV', 'unknown')

if env == 'maya':
    from .menu_bar_maya import MayaMenuBar as MainMenuBar
elif env == 'windows':
    from .menu_bar_windows import WindowsMenuBar as MainMenuBar
else:
    from .base_menu_bar import BaseMenuBar as MainMenuBar
