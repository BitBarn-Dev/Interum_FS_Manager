import os

env = os.environ.get('PRTTM_DCC_ENV', 'unknown')

if env == 'maya':
    from .widgets_maya import TaskTreeContext, OutputTreeContext
elif env == 'rocky':
    from .utils_rocky import TaskTreeContext, OutputTreeContext
elif env == 'windows':
    from .widgets_windows import TaskTreeContext, OutputTreeContext
else:
    raise ImportError(f"Unsupported environment: {env}")
