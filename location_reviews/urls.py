from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, LocationViewSet, ReviewViewSet


router = routers.DefaultRouter()
router.register(r'location', LocationViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = router.urls