from django.contrib import admin

# Register your models here.
from .models import Category, Item, OrderItem, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'start_date', 'ordered_date', 'ordered']

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
