from django.db import models

# Create your models here.

class servers (models.Model): 
    ip = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100, default="")
    task = models.CharField(max_length=100, default="")
    csrf = models.CharField(max_length=100, default="")
    inUse = models.BooleanField(default=False)