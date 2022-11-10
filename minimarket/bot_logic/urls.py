from django.urls import path
import bot_logic.views as bot

urlpatterns = [
    path('', bot.index),
]
