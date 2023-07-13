from decimal import ROUND_DOWN, Decimal
from django.db import models
from django.contrib.auth import get_user_model
from rating.models import Rating

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username
    
    def calculate_avg_rating(self):
        ratings = Rating.objects.filter(item__created_by=self.user)
        if ratings.count() > 0:
            sum_ratings = sum([rating.rating for rating in ratings])
            avg_rating = Decimal(sum_ratings) / ratings.count()
            self.average_rating = avg_rating.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        else:
            self.average_rating = 0
        self.save()
    