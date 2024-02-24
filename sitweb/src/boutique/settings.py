import os

if os.environ['PRODUCTION'] == 'true':
    print("RUNNING IN PRODUCTION")
    from .settings_prod import *
else:
    print("RUNNING IN DEVELOPPEMENT")
    from .settings_dev import *

