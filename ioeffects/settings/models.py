from django.db import models

# Create your models here.

class Effect(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    param = models.IntegerField(default=0)

class Twitter(models.Model):
    status = models.BooleanField(default=False)
    modifier = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
