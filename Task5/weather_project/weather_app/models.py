from django.db import models

# Create your models here.
class Weather(models.Model):
    city = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    temp = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city