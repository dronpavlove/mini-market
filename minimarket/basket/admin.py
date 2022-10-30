from django.contrib import admin
from django.db.models import F

from basket.models import BasketClient
from products.models import Product


@admin.register(BasketClient)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'client', 'product', 'product_amount', 'total_cost', 'flag_paid', 'updated']
    list_filter = ('flag_paid', 'client')
    actions = ['mark_as_item_paid', 'mark_as_item_ex_paid', 'mark_as_item_not_paid']

    def mark_as_item_paid(self, request, queryset):  # надо добавить в историю заказов
        queryset.update(flag_paid='y')

    def mark_as_item_ex_paid(self, request, queryset):
        queryset.update(flag_paid='ex')

    def mark_as_item_not_paid(self, request, queryset):
        id_list = [(i.product.id, i.product_amount, i.client_id) for i in queryset]
        num = 0
        for product_info in id_list:
            full_amount = 0
            product = Product.objects.get(id=product_info[0])
            client_product = BasketClient.objects.filter(product_id=product_info[0], client_id=product_info[2])
            product.amount = F('amount') + product_info[1]
            product.save()
            if len(client_product) > 1:
                for obj in client_product[1::]:
                    full_amount += obj.product_amount
                    obj.delete()
                client_product[0].product_amount = F('product_amount') + full_amount
                client_product[0].save()
            num += 1
        queryset.update(flag_paid='n')

    mark_as_item_paid.short_description = 'перевести в статус "оплачено"'
    mark_as_item_ex_paid.short_description = 'перевести в статус "ожидает оплаты"'
    mark_as_item_not_paid.short_description = 'перевести в статус "неоплачено"'
