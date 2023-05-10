import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "puddle.settings")
import django
django.setup()

from item.models import Item
from core.models import Profile

for item in Item.objects.all():
    item.calculate_avg_rating()

for profile in Profile.objects.all():
    profile.calculate_avg_rating()