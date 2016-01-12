from django.db import models

# Create your models here.
class KeyManager(models.Model):
    phone = models.BigIntegerField(primary_key=True)
    paillier_private = models.CharField(max_length=4096)
    paillier_public = models.CharField(max_length=4096)
    ope_key = models.CharField(max_length=4096)
