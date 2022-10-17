from django.urls import path
from basket.views import basket_add_remove_product, basket_page, basket_delete, ordering


urlpatterns = [
    path('add/', basket_add_remove_product, name='basket_add'),
    path('', basket_page, name='basket_page'),
    path('delete/', basket_delete, name='basket_delete'),
    path('ordering/', ordering, name='ordering')
]
