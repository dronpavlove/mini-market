from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, Update
from telegram.ext import Filters, MessageHandler, Updater, CallbackQueryHandler
from telegram.utils.request import Request

from telegram_bot.views import do_eho, keyboard_handler


class Command(BaseCommand):

	help = 'Телеграмм-бот'

	def handle(self, *args, **options):
		request = Request(
			connect_timeout=0.5,
			# read_timeout=1.0
		)
		bot = Bot(
			request=request,
			token=settings.TEL_TOKEN,
			# base_url=settings.TEL_PROXI
		)

		updater = Updater(
			bot=bot,
			use_context=True
		)

		message_handler = MessageHandler(Filters.text, do_eho)
		buttons_handler = CallbackQueryHandler(callback=keyboard_handler(bot=bot), pass_chat_data=True)

		updater.dispatcher.add_handler(message_handler)
		updater.dispatcher.add_handler(buttons_handler)

		updater.start_polling()
		updater.idle()
