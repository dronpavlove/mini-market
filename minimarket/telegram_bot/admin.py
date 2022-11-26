from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import TelegramClient


@admin.register(TelegramClient)
class TelegramClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_name', 'first_name', 'type']

    def __str__(self):
        return _('Клиенты телеграм')
