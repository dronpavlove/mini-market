from django.urls import path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .tel_bot_logic import send_channel_tel_bot_message
from .views import update_category_product_dict

app_name = 'telegram_bot'

urlpatterns = [
	path("channel_message/<int:pk>/", send_channel_tel_bot_message, name="channel_messag"),
	path("update/", update_category_product_dict, name="tel_bot_update"),
]
