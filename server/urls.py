from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from booking.urls import router as booking_router
from common.generator import OptionSchemaGenerator
from course.urls import router as course_router
from plane.urls import router as plane_router
from transaction.urls import router as transaction_router

router = routers.DefaultRouter()
router.registry = plane_router.registry + booking_router.registry + transaction_router.registry + course_router.registry

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("api/", include(router.urls)),
                  path("redoc/", include("redoc.urls")),
                  path('spec/', get_schema_view(
                      title="Flight Safe",
                      description="Flight safe api spec",
                      version="1.0.0",
                      generator_class=OptionSchemaGenerator
                  ), name='spec'),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
