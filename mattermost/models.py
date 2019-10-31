from django.db import models

# Create your models here.
    
class EntityTeam(models.Model):
    name = models.CharField(max_length=60, unique=True)
    team = models.CharField(max_length=60)

