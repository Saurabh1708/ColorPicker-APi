from django.db import models
# Create your models here.


class Picker(models.Model):
    dominant_color= models.CharField(max_length=30)
    logo_border=models.CharField(max_length=30)
    url=models.URLField()
    #id=models.AutoField(primary_key=True)
