from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramClient(models.Model):

    username = models.CharField(max_length=1000, unique=True, verbose_name=_("username"))
    last_name = models.CharField(max_length=1000, blank=True, verbose_name=_("фамилия"))
    first_name = models.CharField(max_length=1000, blank=True, verbose_name=_("имя"))
    type = models.CharField(max_length=1000, blank=True, verbose_name=_("type"))

    class Meta:
        verbose_name = 'Пользователь телеграм'
        verbose_name_plural = 'Пользователи телеграм'
