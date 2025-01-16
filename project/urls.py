from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from refbooks.api.views import RefbooksListAPIView, RefbookElementsListAPIView, RefbookCheckElementAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Справочники",
        default_version='v1',
        description="API для справочников",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('refbooks/', RefbooksListAPIView.as_view()),
    path('refbooks/<int:id>/', RefbookElementsListAPIView.as_view()),
    path('refbooks/<int:id>/check_element/', RefbookCheckElementAPIView.as_view()),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
