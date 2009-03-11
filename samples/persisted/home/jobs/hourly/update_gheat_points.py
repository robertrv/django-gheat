import os.path
import os, logging
import shutil
from datetime import datetime, timedelta

from django_extensions.management.jobs import HourlyJob

from gheat.models import Point
from gheat import ROOT
import feedparser


feeds = [
    #'http://earthquake.usgs.gov/eqcenter/catalogs/eqs7day-M5.xml',
    'http://www.earthpublisher.com/georss.php',
    ]

class Job(HourlyJob):
    help = 'Calculate the points for the gHeat server, fetching them from an'\
            ' internet public georss service'
    

    def execute(self):
        # We should iterate over all the possible filters, any place to have this possible filters ??? __init__.py ? settings.py ?
        shutil.rmtree(ROOT)
        Point.objects.clear_points() # Should be rethought ... probably is no needed ... or it is ?
        
        total_points = 0
        
        for feed in feeds:
            f = feedparser.parse(feed)
            
            for entry in f.entries:
                Point(uid=entry.id if getattr(entry, 'id', None) else total_points,
                    latitude=entry.geo_lat,
                    longitude=entry.geo_long,
                    density=1,
                    ).save()                
                total_points += 1

        logging.info('Finnished calculating new points, total points: %s'
                    % total_points)
