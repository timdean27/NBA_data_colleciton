# models.py
from django.db import models

class nba_players(models.Model):
    first_name = models.CharField(max_length=100, default='default_first_name')
    last_name = models.CharField(max_length=50, default="default_last_name" )
    href = models.CharField(max_length=50, default="default_href" )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nba_players'
