import logging
import os

from gheat import gheatsettings as settings

from django.core.exceptions import ImproperlyConfigured
from django.db import connection

# Logging config
# ==============

if settings.DEBUG:
    level = logging.INFO
else:
    level = logging.WARNING
logging.basicConfig(level=level) # Ack! This should be in Aspen. :^(
log = logging.getLogger('gheat')


# Configuration
# =============
# Set some things that backends will need.
ALWAYS_BUILD = settings.GHEAT_ALWAYS_BUILD
BUILD_EMPTIES = settings.GHEAT_BUILD_EMPTIES

DIRMODE = settings.GHEAT_DIRMODE
try:
    DIRMODE = int(eval(DIRMODE))
except (NameError, SyntaxError, ValueError):
    raise ImproperlyConfigured("dirmode (%s) must be an integer." % dirmode)

SIZE = 256 # size of (square) tile; NB: changing this will break gmerc calls!
MAX_ZOOM = 31 # this depends on Google API; 0 is furthest out as of recent ver.


# Try to find an image library.
# =============================

BACKEND = None 
BACKEND_PIL = False 
BACKEND_PYGAME = False

_want = settings.GHEAT_BACKEND.lower()
if _want not in ('pil', 'pygame', ''):
    raise ImproperlyConfigured( "The %s backend is not supported, only PIL and "
                            + "Pygame (assuming those libraries are installed)."
                             )

if _want:
    if _want == 'pygame':
        from gheat import pygame_ as backend
    elif _want == 'pil':
        from gheat import pil_ as backend
    BACKEND = _want
else:
    try:
        from gheat import pygame_ as backend
        BACKEND = 'pygame'
    except ImportError:
        try:
            from gheat import pil_ as backend
            BACKEND = 'pil'
        except ImportError:
            raise
            pass
    
    if BACKEND is None:
        raise ImportError("Neither Pygame nor PIL could be imported.")

BACKEND_PYGAME = BACKEND == 'pygame'
BACKEND_PIL = BACKEND == 'pil'

log.info("Using the %s library" % BACKEND)


# Set up color schemes and dots.
# ==============================

color_schemes = dict()          # this is used below
    
_color_schemes_dir = os.path.join(settings.GHEAT_CONF_DIR, 'color-schemes')
for fname in os.listdir(_color_schemes_dir):
    if not fname.endswith('.png'):
        continue
    name = os.path.splitext(fname)[0]
    fspath = os.path.join(_color_schemes_dir, fname)
    color_schemes[name] = backend.ColorScheme(name, fspath)

def load_dots(backend):
    """Given a backend module, return a mapping of zoom level to Dot object.
    """
    return dict([(zoom, backend.Dot(zoom)) for zoom in range(MAX_ZOOM)])
dots = load_dots(backend) # factored for easier use from scripts

# Some util methods
# =================
def translate(root, url):
    """Translate a URL to the filesystem.

    We specifically avoid removing symlinks in the path so that the filepath
    remains under the website root. Also, we don't want trailing slashes for
    directories.

    """
    parts = [root] + url.lstrip('/').split('/')
    return os.sep.join(parts).rstrip(os.sep)

ROOT = settings.GHEAT_MEDIA_ROOT
