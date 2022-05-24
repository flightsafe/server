from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from common.generator import OptionSchemaGenerator

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("plane/", include("plane.urls")),
                  path("redoc/", include("redoc.urls")),
                  path('spec/', get_schema_view(
                      title="Flight Safe",
                      description="Flight safe api spec",
                      version="1.0.0",
                      generator_class=OptionSchemaGenerator
                  ), name='spec'),
                  path("booking/", include("booking.urls")),
                  path("transaction/", include("transaction.urls")),
                  path("course/", include("course.urls")),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
