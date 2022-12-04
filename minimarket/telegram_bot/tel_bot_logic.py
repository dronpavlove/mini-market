import requests
from django.conf import settings
from django.http import HttpResponse

from products.views import get_category_dict, get_products_dict
from .views import category_keyboard, category_product_dict, category_dict


def send_channel_tel_bot_message(request, **kwargs):
	"""Принимает сообщение в текстовом формате
	и отправляет на канал в формате HTML"""
	bot_username = 'BenefitTimebot'
	bot_api_key = settings.TEL_TOKEN
	channel_name = '@BenefitTimeChannel'
	product_dict = get_products_dict(kwargs['pk'])
	reply_message = 'Продолжим...'
	url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage'
	reply_markup = category_keyboard()
	for product in product_dict:
		message = f'<b>{product["name"]}</b>\n' \
		          f'<b>{product["article"]}</b>\n' \
		          f'<i>{product["description"]}</i>\n' \
		          f'<a href="https://benefittime.ru/media/{product["photos"][0]}">' \
		          f'фото {product["photos"][0]}</a>\n\n'
		params = {
			'chat_id': channel_name,
			'text': message,
			'parse_mode': 'HTML',
		}
		requests.get(url, params=params)
	params = {
		'chat_id': channel_name,
		'text': reply_message,
		'reply_markup': reply_markup
	}
	requests.get(url, params=params)
	return HttpResponse(reply_message, status=200)
