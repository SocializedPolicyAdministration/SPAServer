from __future__ import unicode_literals

from django.db import models

# Create your models here.
class RequestAssessment(models.Model):
    respondent = models.BigIntegerField()
    requester = models.BigIntegerField()
    content = models.CharField(max_length=4096)
