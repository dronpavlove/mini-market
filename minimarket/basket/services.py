from basket.models import BasketClient
from datetime import datetime, timedelta


def delete_old_baskets(minites):
    """Удаляем корзинки на сессиях, которые не обновлялись minutes минут"""
    now = datetime.now()
    check_date = now - timedelta(minutes=minites)
    baskets = BasketClient.objects.filter(updated__gte=check_date, client__isnull=True)
    baskets.delete()
