# Let the developer to override generic values for the gheat settings 
# Normally set on a localsettings.py file or the same settings.py of your
# home project
from django.conf import settings

from os.path import dirname, abspath, join
# Default Gheat settings
GHEAT_BACKEND = getattr(settings, 'GHEAT_BACKEND','PIL')
GHEAT_ZOOM_OPAQUE=getattr(settings, 'GHEAT_ZOOM_OPAQUE', -1)
GHEAT_ZOOM_TRANSPARENT=getattr(settings, 'GHEAT_ZOOM_TRANSPARENT', 17)
GHEAT_FULL_OPAQUE=getattr(settings, 'GHEAT_FULL_OPAQUE', True)
GHEAT_BUILD_EMPTIES=getattr(settings, 'GHEAT_BUILD_EMPTIES', True)
GHEAT_ALWAYS_BUILD=getattr(settings, 'GHEAT_ALWAYS_BUILD', True)
GHEAT_DIRMODE = getattr(settings, 'GHEAT_DIRMODE', '0755')

GHEAT_CONF_DIR = getattr(settings, 'GHEAT_CONF_DIR', join(dirname(abspath(__file__)), 'etc'))
GHEAT_MEDIA_ROOT = getattr(settings, 'GHEAT_MEDIA_ROOT', '/tmp/gheat/')
DEBUG = settings.DEBUG


