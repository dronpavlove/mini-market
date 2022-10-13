from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import F

from basket.models import BasketClient
from products.models import Product


def basket_add_remove_product(request):
    product_id = int(request.GET.get('product_id'))
    product_amount = 0
    try:
        update_data = {'client': request.user.client}
    except:
        update_data = {'session': request.session.session_key}
    basket = BasketClient.objects.filter(**update_data, product_id=product_id)

    if request.GET.get('action') == 'add':
        print('Сюда +++++++++++++++++++++++++ пришло')
        # qty = int(request.POST.get('product_qty'))
        if len(basket) != 0:
            product_in_basket = basket[0]
            # product_amount = product_in_basket.product_amount + 1
            # product_in_basket.product_amount = F('product_amount') + 1
            product_in_basket.product_amount += 1
            # product_in_basket.save()
        else:
            product_in_basket = BasketClient(**update_data, product_id=product_id)
            # product_amount = product_in_basket.product_amount
        product_amount = product_in_basket.product_amount
        product_in_basket.save()

    elif request.GET.get('action') == 'remove':
        print('Сюда --------------------- пришло')
        product_in_basket = basket[0]
        # product_in_basket.product_amount = F('product_amount') - 1
        product_in_basket.product_amount -= 1
        product_amount = product_in_basket.product_amount
        product_in_basket.save()

    client_basket = BasketClient.objects.filter(**update_data)
    count_product_in_basket = sum([i.product_amount for i in client_basket])
    full_sum = sum([i.total_cost for i in client_basket])
    print('RESPONSE ++++++++++', product_amount, count_product_in_basket, full_sum)
    response = JsonResponse({
        'product_amount': product_amount,
        'count_product_in_basket': count_product_in_basket,
        'full_sum': full_sum,
    })
    return response


def basket_page(request):
    return render(request, 'basket/basket.html')


def basket_delete(request):
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('productid')
        basket_item = BasketClient.objects.get_item(request=request, product=product_id)
        basket_item.delete()
        client_basket = BasketClient.objects.smart_filter(request=request)
        response = JsonResponse({
            'qty': client_basket.total_count,
            'subtotal': client_basket.total_price,
            'discount_subtotal': client_basket.total_old_price,
        })
        return response
