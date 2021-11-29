from django.db import models

class BotUsers(models.Model):
	user_id  = models.CharField(max_length=50)
	username = models.CharField(max_length=30, null=True, blank=True)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)

