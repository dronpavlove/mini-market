from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.shortcuts import render
from django.conf import settings
from pathlib import Path
# from fpdf import FPDF, HTMLMixin
from datetime import datetime
from basket.models import BasketClient
from accounts.models import Client, Order
from accounts.forms import ClientForm
from .context_processors import basket_client_info
from accounts.forms import RegistrationForm
from products.models import Product


def basket_add_remove_product(request):
    product_id = int(request.GET.get('product_id'))
    product_amount = 0
    product_total_cost = 0
    try:
        update_data = {'client': request.user.client}
    except:
        update_data = {'session': request.session.session_key}
    basket = BasketClient.objects.filter(**update_data, product_id=product_id, flag_paid='n')

    if request.GET.get('action') == 'add':
        if len(basket) != 0:
            product_in_basket = basket[0]
            product_in_basket.product_amount += 1
        else:
            product_in_basket = BasketClient(**update_data, product_id=product_id)
        product_full_amount = Product.objects.get(id=product_id).amount
        if product_in_basket.product_amount > product_full_amount:
            product_in_basket.product_amount = product_full_amount
        product_amount = product_in_basket.product_amount
        product_in_basket.save()
        product_total_cost = product_in_basket.total_cost

    elif request.GET.get('action') == 'remove':
        product_in_basket = basket[0]
        product_in_basket.product_amount -= 1
        product_amount = product_in_basket.product_amount

        if product_amount == 0:
            product_in_basket.delete()
        else:
            product_in_basket.save()
            product_total_cost = product_in_basket.total_cost

    client_basket = BasketClient.objects.filter(**update_data, flag_paid='n')
    count_product_in_basket = sum([i.product_amount for i in client_basket])
    full_sum = sum([i.total_cost for i in client_basket])
    response = JsonResponse({
        'product_amount': product_amount,
        'count_product_in_basket': count_product_in_basket,
        'full_sum': full_sum,
        'product_total_cost': product_total_cost
    })
    return response


def basket_page(request):
    return render(request, 'basket/basket.html')


def basket_delete(request):
    if request.GET.get('action') == 'delete':
        product_id = request.GET.get('product_id')
        try:
            update_data = {'client': request.user.client}
        except:
            update_data = {'session': request.session.session_key}
        basket_item = BasketClient.objects.get(**update_data, product=product_id, flag_paid='n')
        basket_item.delete()

        client_basket = BasketClient.objects.filter(**update_data, flag_paid='n')
        count_product_in_basket = sum([i.product_amount for i in client_basket])
        full_sum = sum([i.total_cost for i in client_basket])
        response = JsonResponse({
            'count_product_in_basket': count_product_in_basket,
            'full_sum': full_sum,
        })
        return response


def ordering(request):

    if request.user.is_authenticated:
        text = str()
        text_table = str()
        if Client.objects.filter(user=request.user).exists():
            client_basket = basket_client_info(request)
            try:
                client = client_basket['basket'][0].client
            except IndexError:
                return HttpResponse('Корзина пуста')
            check_num = client.user.username + '-' + str(datetime.now())
            for i in client_basket['basket']:
                check_num += '-' + str(i.product.id)
                change_in_product_quantity(product_id=i.product.id, count=i.product_amount, product_in_basket=i)
                text_table += f'<tr>\n<th>{i.product.name}</th>\n' \
                              f'<th>{str(i.product_amount)}</th>\n' \
                              f'<th>{str(i.product.price)}</th>\n<th>{str(i.total_cost)}</th>\n</tr>\n'
            text += f'<h4>Общая сумма заказа: {client_basket["full_sum"]}</h4>\n' \
                    f'<h4>{client.user.username}</h4>\n' \
                    f'<h4>телефон: {client.phone}</h4>\n' \
                    f'<h4>Город:   {client.city}</h4>\n' \
                    f'<h4>ул. {client.street}, {client.house_number}, кв. {client.apartment_number}</h4>'

            new_text = save_pdf_file(text=text, text_table=text_table, num=str(check_num))
            check_data = {
                'client': client,
                'number_order': check_num,
                'clients_check': f'check/check-{check_num}.html'
            }
            client_check = Order(**check_data)
            client_check.save()

            return HttpResponse(new_text)
        else:
            return HttpResponseRedirect("/accounts/profile/")

    else:
        return HttpResponseRedirect("/accounts/login/")


def change_in_product_quantity(product_id: int, count: int, product_in_basket):
    product = Product.objects.get(id=product_id)
    product.amount = F("amount") - count
    product.save()
    product_in_basket.flag_paid = 'ex'
    product_in_basket.save()


# class MyFPDF(FPDF, HTMLMixin):
#     pass


def save_pdf_file(text: str, text_table: str, num: str):
    num = num
    file_url = str(Path(settings.MEDIA_ROOT, f'check/check-{num}.html'))
    with open(file_url, 'a') as f:
        new_text = '<!DOCTYPE html>\n<html lang="en">\n<head>\n' \
                   '<meta charset="UTF-8">\n<title>Чек</title>\n</head>\n<body>\n' \
                   '<h2>Ваш заказ: (черновик-набросок)</h2>\n' \
                   '<table border="1">\n<tr>\n<th>Наименование товара</th>\n' \
                   '<th>Количество</th>\n' \
                   '<th>Цена</th>\n<th>Стоимость</th>\n</tr>' \
                   + text_table + '</table>\n' \
                   + text + '\n</body>\n</html>'
        f.write(new_text)
    return new_text
