from django.urls import path
from redoc import views

urlpatterns = [
    path("", views.open_api_view, name="redoc")
]