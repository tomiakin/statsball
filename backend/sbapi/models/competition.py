from django.db import models

class Competition(models.Model):
    """Core competition/league information"""
    competition_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'country')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country']),
        ]

    def __str__(self):
        return f"{self.name} ({self.country})"

class Season(models.Model):
    """Season information for a competition"""
    season_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)  # e.g., "2023/24"
    # start_date = models.DateField()
    # end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('competition', 'name')
        indexes = [
            models.Index(fields=['is_current']),
        ]

    def __str__(self):
        return f"{self.competition.name} {self.name}"