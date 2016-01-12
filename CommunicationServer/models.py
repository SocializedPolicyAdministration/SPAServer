from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Transaction(models.Model):
    class Meta:
        unique_together = (('request', 'respondent'),)

    request = models.BigIntegerField()
    respondent = models.BigIntegerField()
    paillier_n = models.CharField(max_length=4096)
    paillier_g = models.CharField(max_length=4096)
    ope_key = models.CharField(max_length=4096)
    weight = models.CharField(max_length=4096)
    settings = models.CharField(max_length=4096)
    spa_policies = models.CharField(max_length=4096, default='')


