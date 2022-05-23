from django.urls import path, include
from rest_framework import routers

from booking import views

router = routers.DefaultRouter()
router.register(r"booking", views.BookingViewSet)

urlpatterns = [
    path("", include(router.urls))
]
