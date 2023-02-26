import time
import vk_api
from vk_api import VkUpload
from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings
from pathlib import Path

from products.views import get_products_dict, get_category_dict

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()
vk_upload = VkUpload(vk)

timer = 0


def send_message(**kwargs):
	"""
	Отдаёт сообщение пользователю в зависимости от задачи
	(в группу или лично пользователю,
	с клавиатурой или без неё,
	с фото или без фото)
	"""

	post = {
		'keyboard': kwargs['event']['keyboard'],
		'random_id': 0,
		'peer_id': kwargs['event']['from_id'],
		'message': kwargs['message'],
        "buttons":[],"one_time":True
	}
	for element in kwargs:
		if element == 'attachment':
			post['attachment'] = kwargs['attachment']
		elif element == 'keyboard':
			post.pop('keyboard')

	vk.messages.send(**post)


def group_msg(group_id, text, keyboard):
	vk.messages.send(peer_id=group_id, message=text, keyboard=keyboard, random_id=0)


def button_response(section_id: int):
	"""
	В зависимости от выбранной категории (по нажатию кнопки)
	возвращает соответствующую продукцию с описанием, с фотографией
	"""
	products = get_product_objects(section_id)

	if len(products) == 0:
		yield {'message': 'В базе продукция сейчас не найдена. Попробуйте позже...', 'attachment': '543'}
	else:
		for product in products:
			text = str(product['name']) + '\n' + str(product['description'])
			attachment = product['attachment']
			yield {'message': text, 'attachment': attachment}


def get_product_objects(section: int):
	"""
	Возвращает список продукции в зависимости от выбранной категории.
	"""
	full_products = cache.get_or_set('full_products', {})
	if edit_timer() is True or section not in full_products:
		update_data()
# 		full_products = cache.get('full_products')
	products = full_products[section]
	return products


def edit_timer(period=24):
	"""
	Определяет периодичность обновления глобальных переменных
	full_products = dict()
	sections = dict()
	По умолчанию 24 часа
	"""
	global timer
	current_time = int(time.strftime('%H', time.localtime()))
	if current_time > timer:
		difference = current_time - timer
	else:
		difference = 24 - timer + current_time
	if difference >= period:
		timer = current_time
		return True
	else:
		return False


def send_photo(url):
	"""
	Расширяет объект Product полем 'attachment'
	(прогружает фото в ВК и сохраняет данные для
	ускорения отправки ответных сообщений)
	"""
	upload = vk_api.VkUpload(vk)
	photo_url = str(Path(settings.MEDIA_ROOT, url))
	try:
		photo = upload.photo_messages(photo_url)
	except:
		photo = cache.get('default_photo')
		if not photo:
			photo = upload.photo_messages(str(Path(settings.MEDIA_ROOT, 'defolt.png')))
			cache.set('default_photo', photo)

	owner_id = photo[0]['owner_id']
	photo_id = photo[0]['id']
	access_key = photo[0]['access_key']
	attachment = f'photo{owner_id}_{photo_id}_{access_key}'
	return attachment


def update_data(request=None):
	"""
	Возвращает список продукции в зависимости от выбранной категории.
	Обращается или к БД (длительный процесс),
	или к глобальной переменной (для ускорения процесса)
	"""
	full_products = cache.get_or_set('full_products', {})
	sections = get_category_dict()
	for section_id in sections.values():
		product_list = get_products_dict(section_id)
		if section_id not in full_products:
			products = [{
				'name': i['name'], 'article': i['article'], 'description': i['description'], 'photo': i['photos'][0],
				'attachment': send_photo(i['photos'][0]) # str(Path(settings.MEDIA_ROOT, i['photos'][0]))
			} for i in product_list]
			full_products[section_id] = products
		else:
			photo_list = [i['photo'] for i in full_products[section_id]]
			article_list = [i['article'] for i in full_products[section_id]]
			for product in product_list:
				if product['photos'][0] not in photo_list and product['article'] not in article_list:
					new_product = {
						'name': product['name'],
						'article': product['article'],
						'description': product['description'],
						'photo': product['photos'][0],
						'attachment': send_photo(product['photos'][0])
					}
					full_products[section_id].append(new_product)
				elif product['photos'][0] not in photo_list and product['article'] in article_list:
					for old_product in full_products[section_id]:
						if old_product['article'] == product['article']:
							old_product['photo'] = product['photos'][0]
							old_product['attachment'] = send_photo(product['photos'][0])
	cache.set('full_products', full_products)
	cache.set('sections', sections)
	return HttpResponse('Кэш обновился' + str(cache.get('full_products')) + '\n' + str(cache.get('sections')), status=200)
