from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    auction = models.ForeignKey('List', on_delete=models.CASCADE, related_name='product_bids')
    cost = models.IntegerField(max_length=6)

    def __str__(self):
        return f"{self.user} bids for ${self.cost}"

class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    commentInput = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.comment_user}: {self.commentInput}"

class List(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=64)
    price = models.IntegerField(max_length=6)
    bids = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, related_name="bidders", null=True)
    comments = models.ManyToManyField(Comment, related_name="comments", blank=True)
    imguser = models.CharField(max_length=64)
    image = models.ImageField(upload_to='photos/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    category = models.CharField(max_length=64)
    closed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title}, Costs: {self.price},  Seller: {self.owner}"

class WatchList(models.Model):
    watch_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_watchlist')
    auctions = models.ManyToManyField('List', related_name='list_watchlist', blank=True)
    def __str__(self):
        return f"{self.user} personal watchlist"




    

