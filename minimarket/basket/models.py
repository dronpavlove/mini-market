from django.db import models
from django.db.models import Manager, QuerySet, Sum
from django.utils.translation import gettext_lazy as _
from django.db.models import F

from products.models import Product
from accounts.models import Client


class BasketClient(models.Model):
    STATUS_CHOICES = [
        ('y', _('оплачен')),
        ('ex', _('ожидает оплаты')),
        ('n', _('неоплачен'))
    ]
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Продукт'),
        related_name='basket_items',
        null=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_('Клиент'),
        related_name='basket_items',
        null=True, blank=True
    )
    product_amount = models.PositiveSmallIntegerField(
        _("Количество"),
        default=1
    )
    total_cost = models.DecimalField(
        _('Общая стоимость'),
        max_digits=9,
        decimal_places=2,
        default=0
    )
    session = models.CharField(
        max_length=256,
        verbose_name=_('Ключ сессии'),
        blank=True, null=True,
    )
    flag_paid = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='n',
        verbose_name=_('статус оплаты')
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее обновление'
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.total_cost = self.product.price * self.product_amount
        super(BasketClient, self).save(*args, **kwargs)
