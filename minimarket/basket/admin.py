from django.contrib import admin

from basket.models import BasketClient


@admin.register(BasketClient)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'client', 'product', 'product_amount', 'total_cost', 'updated']
