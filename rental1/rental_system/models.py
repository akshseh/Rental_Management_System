from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
	is_owner = models.BooleanField(default = False)
	def __str__(self):
		res = str(self.username)
		return res

class Property(models.Model):
	id = models.AutoField(primary_key = True) 
	description = models.TextField(default = '',blank = False)
	price = models.IntegerField(blank = False)
	location = models.CharField(max_length = 50,blank = False,null = False) 
	num_views = models.IntegerField(default=0)
	avg_rating = models.IntegerField(default=0)
	owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

class Visitor(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	id = models.AutoField(primary_key = True)
	profile = models.TextField(blank = False)
	pref_location = models.CharField(max_length = 30) 

class Owner(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	id = models.AutoField(primary_key = True)
	num_properties = models.IntegerField(default=0)
	owner_name = models.CharField(max_length=30)

class Rented(models.Model):
	owner_id = models.ForeignKey('rental_system.Owner',on_delete = models.CASCADE )
	prop_id = models.ForeignKey('rental_system.Property',on_delete = models.CASCADE )
	visitor_id = models.ForeignKey('rental_system.Visitor',on_delete = models.CASCADE )
	rent_to_be_paid = models.IntegerField(default=0)

class Review(models.Model):
	prop_id = models.ForeignKey('rental_system.Property',on_delete = models.CASCADE )
	visitor_id = models.ForeignKey('rental_system.Visitor',on_delete = models.CASCADE )
	visitor_name = models.CharField(max_length = 30, blank = False)
	rating = models.IntegerField(default=0)
	comment = models.CharField(max_length = 100,blank = False)