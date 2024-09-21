from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Unicum API",
        default_version='v1',
        description="Unicum Academy Test system API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ilhomjonpersonal@gmail.com"),
        license=openapi.License(name="Unicum License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('api/docs/redoc/', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)