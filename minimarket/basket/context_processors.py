from basket.models import BasketClient


def basket_client_info(request):
    """
    При помощи этого контекст процессора на странице всегда есть инфа о корзине
    """
    count_product_in_basket = 0
    session_key = request.session.session_key
    full_sum = 0
    if not session_key:
        request.session.cycle_key()
    try:
        basket = BasketClient.objects.select_related('product', 'client').filter(
            client=request.user.client, flag_paid='n'
        )
    except:
        basket = BasketClient.objects.select_related('product').filter(
            session=session_key, flag_paid='n'
        )
    if len(basket) != 0:
        count_product_in_basket += sum([i.product_amount for i in basket])
        full_sum += sum([i.total_cost for i in basket])

    return {'basket':  basket, 'count_product_in_basket': count_product_in_basket, 'full_sum': full_sum}
