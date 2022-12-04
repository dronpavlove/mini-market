from django.urls import path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .tel_bot_logic import send_channel_tel_bot_message
from .views import update_category_product_dict
from .tel_bot_wh import index, restart_webhook

app_name = 'telegram_bot'

urlpatterns = [
	path("channel_message/<int:pk>/", send_channel_tel_bot_message, name="channel_message"),
	path("message/", index, name="message"),
	path("webhook/", restart_webhook, name="webhook"),
	path("update/", update_category_product_dict, name="tel_bot_update"),
]
