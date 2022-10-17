from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.safestring import mark_safe
from accounts.models import Client, ClientProductView
from django.utils.translation import gettext_lazy as _


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_seller', 'limit_items_views',
                    'item_in_page_views']
    list_filter = ['is_seller']
    list_display_links = ['user']
    exclude = ("deleted_at",)
    search_fields = ['^name', ]
    # readonly_fields = ('orders',)
    autocomplete_fields = ['item_view']
    list_editable = ['limit_items_views', 'item_in_page_views']

    # @staticmethod
    # @admin.display(description=_("Количество заказов"))
    # def get_orders_count(obj: Client):
    #     orders = obj.orders.count()
    #     return orders

    # @staticmethod
    # @admin.display(description=_('Аватарка'))
    # def client_photo(obj: Client):
    #     if not obj.photo:
    #         return 'Нету фотографии'
    #     return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.photo.url))


@admin.register(ClientProductView)
class ClientProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'product', 'created_dt']
    list_filter = ['client']
    list_display_links = ['client']
