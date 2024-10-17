from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name

