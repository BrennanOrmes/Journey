from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    public = models.BooleanField()
    price = models.nullIntegerField(max_length=10, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class User(models.Model):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)

class Location(models.Model):
    coordinates = models.FloatField(max_length=20) #momentarily not used
    name = models.CharField(max_length=255)
    opentime = models.TimeField(null=True)
    closedtime = models.TimeField(null=True)
    
class Tags(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    