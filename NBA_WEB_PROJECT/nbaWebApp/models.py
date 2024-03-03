# models.py
from django.db import models

class NBA_PLAYERS(models.Model):
    full_name = models.CharField(max_length=255, default='default_full_name')
    first_name = models.CharField(max_length=255, default='default_first_name')
    last_name = models.CharField(max_length=255, default='default_last_name')
    href = models.CharField(max_length=255, unique=True, default='default_href')
    img_src = models.CharField(max_length=255, default='default_img_src')
    ppg = models.FloatField(default=0.0)  
    apg = models.FloatField(default=0.0)  
    rpg = models.FloatField(default=0.0)  
    pie = models.FloatField(default=0.0) 


    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'nba_players'
