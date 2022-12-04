from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import json
from vkbottle import Keyboard, Text

from bot_logic.vk_bot_logic import send_message, button_response, group_msg
from products.views import get_category_dict


@csrf_exempt
def index(request):
	if request.method == "POST":
		section_dict = get_category_dict()
		data = json.loads(request.body.decode('utf-8'))
		message_data = data['object']['message']
		keyboard = Keyboard(one_time=False, inline=True)
		i = 0
		for elem, value in section_dict.items():
			if i % 3 != 0:
				keyboard.add(Text(elem))
			else:
				keyboard.row()
				keyboard.add(Text(elem))
			i += 1
		message_data['keyboard'] = keyboard.get_json()
		clean_text = message_data['text']
		if data['type'] == 'confirmation':  # if VK server request confirmation
			return settings.VK_GET_KEY

		elif data['type'] == 'message_new':

			if clean_text in section_dict:
				category_id = section_dict[clean_text]
				send_message(
					message=f'Запрос принят. Минуточку... Сейчас обрабатывается запрос {clean_text}: id={category_id}',
					event=message_data, keyboard=False
				)
				for i in button_response(category_id):
					send_message(message=i['message'], event=message_data, attachment=i['attachment'], keyboard='None')

				send_message(message='Продолжим...', event=message_data)

				return HttpResponse('ok', content_type="text/plain", status=200)
			else:
				start_text = f'Представляю Вашему вниманию витрину магазина Benefittime.ru' \
				             f'\nВыберете интересующую ктегорию на клавиатуре' \
				             f'\nОтвет отправлю в личные сообщения' \
				             f'\nПерейти на сайт: https://benefittime.ru/'
				group_msg(group_id=215851367, text=start_text, keyboard=message_data['keyboard'])
				return HttpResponse('ok', content_type="text/plain", status=200)
	else:
		return HttpResponse('see you :)')
