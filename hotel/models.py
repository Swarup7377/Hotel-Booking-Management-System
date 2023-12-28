from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    categoryname = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    def __str__(self):
        return self.categoryname


class Room(models.Model):
    roomtype = models.ForeignKey(Category, on_delete=models.CASCADE)
    roomname = models.CharField(max_length=100)
    maxadult = models.IntegerField()
    maxchild = models.IntegerField()
    roomdescription = models.CharField(max_length=500)
    noofbed = models.IntegerField()
    image = models.FileField()
    roomfacility = models.CharField(max_length=500)
    def __str__(self):
        return self.id

class Booking(models.Model):
    roomid = models.ForeignKey(Room, on_delete=models.CASCADE)
    bookingnumber = models.CharField(max_length=100)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    idtype = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    checkindate = models.DateField()
    checkoutdate = models.DateField()
    bookingdate = models.DateField()
    remark = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    def __str__(self):
        return self.bookingnumber

class Facility(models.Model):
    facilitytitle = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.FileField()
    def __str__(self):
        return self.facilitytitle

class Contact(models.Model):
    name = models.CharField(max_length=50)
    mobilenumber = models.CharField(max_length=10)
    emailid = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    enquirydate = models.DateField()
    isread = models.CharField(max_length=10)
    def __str__(self):
        return self.name

