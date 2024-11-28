from django.db import models

class Competition(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    
    class Meta:
        unique_together = ('name', 'country', 'season')
    
    def __str__(self):
        return f"{self.name} {self.season}"