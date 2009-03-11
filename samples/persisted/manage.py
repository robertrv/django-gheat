#!/usr/bin/env python
from django.core.management import execute_manager
import sys
from os.path import dirname, abspath, join

# Importing gheat folder to be more easy to test this application. In a real 
# application should be done with python_path
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

# Importing also django extenions

sys.path.append(join(dirname(dirname(dirname(abspath(__file__)))),'external','django-extensions'))


try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
