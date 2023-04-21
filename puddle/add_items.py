import os
import django
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "puddle.settings")
django.setup()

from item.models import Item, Category
from django.contrib.auth.models import User

input_dir = 'C:/Users/KimAnh/Desktop/anh_item/clother_items/'

for filename in os.listdir(input_dir):
    if filename.endswith('.jpg'):
        # Parse the attributes from the filename
        name, price, user_id = filename[:-4].split('_')
        item_data = {
            'category': Category.objects.get(name='Clothers'),
            'name': name,
            'description': f"Description for {name}",
            'price': float(price),
            'image': f'item_images/{filename}',
            'is_sold': False,
            'created_by': User.objects.get(id=int(user_id)),
        }
        item = Item(**item_data)
        item.save()
        print(f"Added {item.name}")

        # Copy the image to the item_images directory
        src_path = os.path.join(input_dir, filename)
        dest_path = os.path.join('C:/Users/KimAnh/Desktop/PUDDLE/puddle/media/', 'item_images', filename)
        shutil.copyfile(src_path, dest_path)
        print(f"Copied {filename} to item_images directory")