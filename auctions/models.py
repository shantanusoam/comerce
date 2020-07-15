from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime



class User(AbstractUser):
    pass

class Listing(models.Model):
	title = models.CharField(max_length=20)
	description = models.CharField(max_length=200)
	starting_bid = models.IntegerField()
	image_path = models.CharField(max_length=80)
	category = models.CharField(max_length=10)
	time = models.DateTimeField(default=datetime.datetime.now)
	bidding_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user")

	def __str__(self):
		return f"{self.title} = {self.description}"

class Bids(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bidder")
	auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "item")
	bid = models.IntegerField()

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
	auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented_item")
	comment = models.CharField(max_length=100)