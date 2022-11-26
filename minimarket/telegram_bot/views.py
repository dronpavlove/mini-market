from telegram import Bot, Update, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

from products.views import get_category_dict, get_products_dict
from telegram_bot.models import TelegramClient


def log_errors(f):
	def inner(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except Exception as e:
			error_message = f'-----ERROR-----Произошла ошибка {e}\n\n'
			print(error_message)
			raise e

	return inner


@log_errors
def do_eho(update: Update, context: CallbackContext, **kwargs):
	text = update.message.text  # это текст из сообщения
	reply_text = get_product_html_info(text)
	category_dict = get_category_dict()

	user_info = {
		'username': update.message.chat.username,
		'first_name': str(update.message.chat.first_name),
		'id': update.message.chat.id,
		'last_name': str(update.message.chat.last_name),
		'type': update.message.chat.type
	}
	if not TelegramClient.objects.filter(id=user_info['id']).exists():
		TelegramClient.objects.create(**user_info)

	reply_markup = category_keyboard(category_dict)  # category_callback(category_dict)
	update.message.reply_text(
		text=reply_text, parse_mode='HTML', reply_markup=reply_markup
	)


def get_product_html_info(text: str):
	category_dict = get_category_dict()
	reply_text = str()
	if text in category_dict:
		product_dict = get_products_dict(category_dict[text])
		for product in product_dict:
			text_to_html = f'<b>{product["name"]}</b>\n' \
			               f'<b>{product["article"]}</b>\n' \
			               f'<i>{product["description"]}</i>\n' \
			               f'<a href="https://benefittime.ru/media/{product["photos"][0]}">' \
			               f'фото {product["photos"][0]}</a>\n\n'
			reply_text = "Есть такая категория\n" + text_to_html
	else:
		reply_text = '<b>Нет такой категории\n' + text + '</b>'

	return reply_text


def category_callback(category_dict: dict):
	# {category_name: id}
	keyboard = []
	inline_keyboard = []
	num = 1
	for category in category_dict:
		if num % 4 != 0:
			inline_keyboard.append(InlineKeyboardButton(category, callback_data=category_dict[category]))
		else:
			inline_keyboard.append(InlineKeyboardButton(category, callback_data=category_dict[category]))
			keyboard.append(inline_keyboard)
			inline_keyboard = []
		num += 1
	keyboard.append(inline_keyboard)
	reply_markup = InlineKeyboardMarkup(keyboard)
	return reply_markup


def category_keyboard(category_dict: dict):
	keyboard = []
	inline_keyboard = []
	num = 1
	for category in category_dict:
		if num % 3 != 0:
			inline_keyboard.append(KeyboardButton(category))
		else:
			inline_keyboard.append(KeyboardButton(category))
			keyboard.append(inline_keyboard)
			inline_keyboard = []
		num += 1
	keyboard.append(inline_keyboard)
	reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, inline_keyboard=False)
	return reply_markup


def keyboard_handler(chat_data=None, **kwargs):
	pass
# 	update = Update
# 	query = update.callback_query
# 	print('/////', '\n********', query)
# 	try:
# 		data = query.data
# 		chat_id = update.effective_message.chat_id
# 		curent_tex = update.message.text
#
# 		kwargs['bot'].send_message(chat_id=chat_id, text='data', reply_markup=category_callback(get_category_dict()))
# 	except:
# 		pass
