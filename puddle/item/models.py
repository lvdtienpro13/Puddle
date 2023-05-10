from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from payment.models import ShippingAddress
from django.utils import timezone
from django.db.models import Sum


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_add_to_cart_url(self):
        return reverse("item:add-to-cart", kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("item:remove-from-cart", kwargs={
            'pk': self.pk
        })
    def get_orderitem_quantity(self):
        total_quantity = OrderItem.objects.filter(item_id=self.id, ordered=True).aggregate(Sum('quantity'))['quantity__sum']
        return total_quantity if total_quantity else 0
    
    def calculate_avg_rating(self):
        from rating.models import Rating
        ratings = Rating.objects.filter(item=self)
        if ratings.count() > 0:
            sum_ratings = sum([rating.rating for rating in ratings])
            self.average_rating = sum_ratings / ratings.count()
        else:
            self.average_rating = 0
        self.save()
    
    
class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    rated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def __init__(self, *args, **kwargs):
        ordered_date = kwargs.pop('ordered_date', None)
        super().__init__(*args, **kwargs)
        self.ordered_date = ordered_date

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    def complete_order(self):
        # Set ordered to True for all order items in this order
        for item in self.items.all():
            item.ordered = True
            item.save()
        self.ordered = True
        self.ordered_date = timezone.now()
        self.save()


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
