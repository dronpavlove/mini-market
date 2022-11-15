from django.urls import path
import bot_logic.views as bot
from .vk_bot_logic import update_data

urlpatterns = [
    path('', bot.index),
    path('update', update_data)
]
