import os.path
from django.http import HttpResponseRedirect
from gheat import dots
from gheat import backend, color_schemes, translate, ROOT, log, \
        ALWAYS_BUILD

from django.http import HttpResponseBadRequest
from django.conf import settings
from django.views.static import serve

# Create your views here.
def serve_tile(request,color_scheme,zoom,x,y):
    '''
        Responsible for serving png files of the tile for the heat map

        This view will try to serve the file from the filesystem in case already
        exists otherwise just try to genereate it, and serve it.
    '''

    # Asserting request is a correct one
    try:
        assert color_scheme in color_schemes, ( "bad color_scheme: "
                                              + color_scheme
                                               )
        assert zoom.isdigit() and x.isdigit() and y.isdigit(), "not digits"
        zoom = int(zoom)
        x = int(x)
        y = int(y)
        assert 0 <= zoom <= 30, "bad zoom: %d" % zoom
    except AssertionError, err:
        return HttpResponseBadRequest()

    # @TODO: We should return the file in case is already present
    # Also we have to implement a redirection to the front end in case we are not in debug mode ... should we ? 

    fspath = generate_tile(request,color_scheme,zoom,x,y)

    if settings.DEBUG:
        return serve(request, fspath, '/')
    else:
        return HttpResponseRedirect(fspath.replace(ROOT, '/site_media/gheat/'))


def generate_tile(request,color_scheme,zoom,x,y):
    '''
        This view will generate the png file for the current request
    '''
    path = request.path

    path = path[path.index(color_scheme)-1:] # Removing the /gheat/ from the url

    fspath = translate(ROOT, path)

    if os.path.exists(fspath):
        return fspath

    color_scheme = color_schemes[color_scheme]
    tile = backend.Tile(color_scheme, dots, zoom, x, y, fspath)
    if tile.is_empty():
        fspath = color_scheme.get_empty_fspath(zoom)
        log.debug('serving empty tile, request: %s, file %s' % (path,fspath))
    elif tile.is_stale() or ALWAYS_BUILD:
        log.debug('rebuilding %s' % path)
        tile.rebuild()
        tile.save()
    else:
        log.debug('serving cached tile %s' % path)

    return fspath
