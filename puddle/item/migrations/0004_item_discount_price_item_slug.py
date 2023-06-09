# Generated by Django 4.1.7 on 2023-04-13 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
