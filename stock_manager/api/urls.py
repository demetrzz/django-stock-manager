from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DealsViewSet, BondsViewSet

router = DefaultRouter()
router.register(r'deals', DealsViewSet)
router.register(r'bonds', BondsViewSet, basename='bonds')


urlpatterns = [
    path('', include(router.urls)),
]
