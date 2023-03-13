from rest_framework import routers
from site_api.api import UserViewSet, ProductViewSet, CategoryViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('products', ProductViewSet)
router.register('category', CategoryViewSet)

urlpatterns = router.urls + []
