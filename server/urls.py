from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("plane/", include("plane.urls")),
    path("redoc/", include("redoc.urls")),
    path('spec/', get_schema_view(
        title="Flight Safe",
        description="Flight safe api spec",
        version="1.0.0"
    ), name='spec'),
]
