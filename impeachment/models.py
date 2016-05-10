from __future__ import unicode_literals
from django.db import models

class Elector(models.Model):
	register_id = models.CharField(unique=True, max_length=12)
	created_at = models.DateTimeField(auto_now_add=True)
	vote = models.IntegerField()
	
	def __str__(self):
		return str(self.register_id)

