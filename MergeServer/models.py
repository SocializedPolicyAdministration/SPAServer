from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Results(models.Model):
    requester = models.BigIntegerField()
    values = models.TextField()
    count = models.IntegerField(default=1)
    start_time = models.DateTimeField(default=datetime.now)
    spa_policies = models.CharField(max_length=4096)
    n_square = models.TextField()
    settings = models.TextField()