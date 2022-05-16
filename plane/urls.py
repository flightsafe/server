from django.urls import path, include
from rest_framework import routers
from plane import views

router = routers.DefaultRouter()
router.register(r"plane", views.PlaneViewSet)
router.register(r"maintenance", views.MaintenanceViewSet)
router.register(r"maintenance-item", views.MaintenanceRecordItemViewSet)

urlpatterns = [
    path("", include(router.urls))
]