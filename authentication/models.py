
from django.db import models
from django.contrib.auth.models import User


class PassengerTable(models.Model):
    username1 = models.CharField()
    username2 = models.CharField()
    source = models.CharField(max_length=100, null=True)
    destination = models.CharField(max_length=100, null=True)
    date = models.DateField(max_length=20, null=True)
    time = models.TimeField(max_length=20, null=True)
    finished = models.BooleanField(default=False)  # Field to track if the ride is finished
    def __str__(self):
        return self.username1 

class PublisherTable(models.Model):
    username = models.CharField(max_length=20, null=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    source = models.CharField(max_length=100, null=True)
    destination = models.CharField(max_length=100, null=True)
    date = models.DateField(max_length=20, null=True)
    time = models.TimeField(max_length=20, null=True)
    wheele = models.IntegerField(null=True)
    vehicle = models.CharField(null=True)
    seats = models.CharField(null=True,blank=True,default=1)
    discription = models.CharField(null=True,blank=True,default="NONE")
    req1 = models.CharField(null=True,blank=True,default="NONE")
    req2= models.CharField(null=True,blank=True,default="NONE")
    req3 = models.CharField(null=True,blank=True,default="NONE")
    requested_by=models.CharField(null=True,blank=True,default="NONE")
    finished = models.BooleanField(default=False)  # Field to track if the ride is finished

    def __str__(self):
        return self.username

class ClientTable(models.Model):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    sumofrating = models.IntegerField(default=0)
    ppl=models.IntegerField(default=0)
    age = models.IntegerField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email= models.CharField(blank=True, null=True,default="none")

    def __str__(self):
        return self.username      

class PublisherDTable(models.Model):
    username1 = models.CharField(max_length=150)
    username2= models.CharField(max_length=150)

    def __str__(self):
        return self.username2    

class PassengerDTable(models.Model):
    username1 = models.CharField(max_length=150)
    username2= models.CharField(max_length=150)

    def __str__(self):
        return self.username1             



       

      