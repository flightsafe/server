from django.urls import path, include
from rest_framework import routers

from plane import views

router = routers.DefaultRouter()
router.register(r"plane", views.PlaneViewSet, basename="plane")
router.register(r"maintenance", views.MaintenanceViewSet, basename="maintenance")
router.register(r"maintenance-item", views.MaintenanceRecordItemViewSet, basename="maintenance-item")

urlpatterns = [
    path("", include(router.urls))
]
