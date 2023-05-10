from django.db import models
from django.contrib.auth.models import User
from item.models import Item, OrderItem
from django.core.validators import MaxValueValidator, MinValueValidator


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='user_rating', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='item_rating', on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, related_name='oder_item_rating', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    rating_comment = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.name} - {self.rating} stars"