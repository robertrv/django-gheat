from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
OPAQUE = 255
TRANSPARENT = 0


def _build_zoom_mapping(MAX_ZOOM=31):
    """Build and return the zoom_to_opacity mapping
    """
    if MAX_ZOOM is None:
        from gheat import MAX_ZOOM # won't use these in testing
        from django.conf import settings

    zoom_opaque = getattr(settings, 'GHEAT_ZOOM_OPAQUE', -15)

    try:
        zoom_opaque = int(zoom_opaque)
    except ValueError:
        raise ImproperlyConfigured("zoom_opaque must be an integer.")
    
    zoom_transparent = getattr(settings, 'GHEAT_ZOOM_TRANSPARENT', 15)
    try:
        zoom_transparent = int(zoom_transparent)
    except ValueError:
        raise ImproperlyConfigured("zoom_transparent must be an integer.")

    num_opacity_steps = zoom_transparent - zoom_opaque
    zoom_to_opacity = dict()
    if num_opacity_steps < 1:               # don't want general fade
        for zoom in range(0, MAX_ZOOM + 1):
            zoom_to_opacity[zoom] = None
    else:                                   # want general fade
        opacity_step = OPAQUE / float(num_opacity_steps) # chunk of opacity
        for zoom in range(0, MAX_ZOOM + 1):
            if zoom <= zoom_opaque:
                opacity = OPAQUE 
            elif zoom >= zoom_transparent:
                opacity = TRANSPARENT
            else:
                opacity = int(OPAQUE - ((zoom - zoom_opaque) * opacity_step))
            zoom_to_opacity[zoom] = opacity

    return zoom_to_opacity

def _opaque_zoom_mapping(settings=None, MAX_ZOOM=31):
    """Build and return the zoom_to_opacity mapping
    """
    if MAX_ZOOM is None:
        from gheat import MAX_ZOOM # won't use these in testing
        
    zoom_to_opacity = dict()
    for zoom in range(0, MAX_ZOOM + 1):
        zoom_to_opacity[zoom] = OPAQUE

    return zoom_to_opacity
        
full_opaque = getattr(settings, 'GHEAT_FULL_OPAQUE', True)

if full_opaque:
    zoom_to_opacity = _opaque_zoom_mapping()
else:
    zoom_to_opacity = _build_zoom_mapping()

