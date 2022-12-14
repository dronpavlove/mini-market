# Generated by Django 4.0.1 on 2022-11-24 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=1000, unique=True, verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=1000, unique=True, verbose_name='фамилия')),
                ('first_name', models.CharField(blank=True, max_length=1000, unique=True, verbose_name='имя')),
                ('type', models.CharField(blank=True, max_length=1000, unique=True, verbose_name='type')),
            ],
            options={
                'verbose_name': 'Пользователь телеграм',
                'verbose_name_plural': 'Пользователи телеграм',
            },
        ),
    ]
