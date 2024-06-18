import os

env = os.environ.get('PRTTM_DCC_ENV', 'unknown')

if env == 'maya':
    from .publisher_maya import PublisherMaya as Publisher
else:
    from .publisher_base import PublisherBase as Publisher
