from django.db import models


# Create your models here.
class ScoreList(models.Model):

    customer_id = models.SmallIntegerField()
    score = models.SmallIntegerField()
