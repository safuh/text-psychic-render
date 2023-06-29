from django.db import models

# Create your models here.

class Ledger(models.Model):
	email = models.EmailField()
	date = models.DateField()
	amount = models.IntegerField()
	expiry = models.DateField()
	userid = models.IntegerField()
	api_key = models.TextField()
	package = models.IntegerField()
	tokens = models.IntegerField()

		
