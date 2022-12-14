"""minimarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import start_page

urlpatterns = [
    path('', start_page),
    path('admin/', admin.site.urls),
    path("products/", include("products.urls")),
    path("basket/", include("basket.urls")),
    path("accounts/", include("accounts.urls")),
    path('bot/', include('bot_logic.urls')),
    path('tel_bot/', include('telegram_bot.urls'))
]
if settings.DEBUG:
    # static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
