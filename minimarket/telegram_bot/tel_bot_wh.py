from django.conf import settings
from django.http import HttpResponse, Http404

import telebot
from telebot import types


token = settings.TEL_TOKEN
bot = telebot.TeleBot(token)


def restart_webhook(request):
	bot.remove_webhook()
	bot.set_webhook(url=f'https://api.telegram.org/bot{token}/setwebhook?url=https://benefittime.ru/message',
	                certificate=open('./webhook_cert.pem', 'r'))
	if request.headers.get('content-type') == 'application/json':
		update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
		bot.process_new_updates([update])
		return HttpResponse('Получен джейсон', status=200)

	if request.method == 'POST':
		return HttpResponse('Ok', status=200)


def index(request):
	if 'content-length' in request.headers and \
			'content-type' in request.headers and \
			request.headers['content-type'] == 'application/json':
		length = int(request.headers['content-length'])
		json_string = request.body.read(length).decode("utf-8")
		update = telebot.types.Update.de_json(json_string)
		# Эта функция обеспечивает проверку входящего сообщения
		bot.process_new_updates([update])
		return ''
	else:
		raise Http404


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(content_types=['text'])
def start_message(message):
	bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['button'])
def button_message(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Кнопка")
	markup.add(item1)
	bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
	bot.infinity_polling()
# import requests
# from django.conf import settings
# from django.http import HttpResponse
#
# from products.views import get_category_dict, get_products_dict
# from .views import category_keyboard, category_product_dict, category_dict, do_eho
#
#
# updater.start_webhook(listen='0.0.0.0',
#                       port=8443,
#                       url_path='TOKEN',
#                       key='private.key',
#                       cert='cert.pem',
#                       webhook_url='https://example.com:8443/TOKEN')
#
#
# def send_wh_message(request):
# 	"""Принимает сообщение в текстовом формате
# 	и отправляет на канал в формате HTML"""
# 	bot_username = 'BenefitTimebot'
# 	bot_api_key = settings.TEL_TOKEN
# 	channel_name = '@BenefitTimeChannel'
# 	reply_message = 'Пробный текст'
# 	url = f'https://api.telegram.org/bot{bot_api_key}/setwebhook?url=https://benefittime.ru/message'
# 	reply_markup = category_keyboard()
# 	params = {
# 		'chat_id': channel_name,
# 		'text': reply_message,
# 		'parse_mode': 'HTML',
# 		'reply_markup': reply_markup
# 	}
# 	requests.get(url, params=params)
#
# 	if request.method == 'GET':
# 		url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage'
# # 		reply_markup = category_keyboard()
# 		params = {
# 			'chat_id': channel_name,
# 			'text': reply_message,
# 			'parse_mode': 'HTML',
# # 			'reply_markup': reply_markup
# 		}
# 		requests.get(url, params=params)
#
# 	if request.headers.get('content-type') == 'application/json':
# 		url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage'
# # 		reply_markup = category_keyboard()
# 		params = {
# 			'chat_id': channel_name,
# 			'text': 'NOT TEXT',
# 			'parse_mode': 'HTML',
# # 			'reply_markup': reply_markup
# 		}
# 		requests.get(url, params=params)
#
# 	return HttpResponse('ok', status=200)
