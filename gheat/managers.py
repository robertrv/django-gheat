# -*- coding: utf-8 -*-
from django.db import models

class PointManager(models.Manager):

    def actives(self):
        return self.all()

    def points_inside(self,tile):
        '''
            Search all the points inside the Tile
        '''
        lat1, lat2, lng1, lng2 = tile.llbound
        qs = self.filter(
            latitude__lte=lat1,
            latitude__gte=lat2,
            longitude__lte=lng1,
            longitude__gte=lng2,
            density__gt=0,
            )
        return qs

    def num_points(self,tile,modtime=None):
        '''
            Count the number of points in a tile for a certain time
        '''
        qs = self.points_inside(tile)
        if modtime:
            qs.filter(modtime__gt=modtime)

        return qs.count()


    def clear_points(self):
        '''
            Clear all the points of the database
        '''
        self.actives().delete()

