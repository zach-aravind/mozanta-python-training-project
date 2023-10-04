from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("api-auth/", include("rest_framework.urls")),
                  path("", include("users.urls", namespace="users")),
                  path("post/", include("blog_posts.urls", namespace="blog_posts")),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                          schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
                       name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
                       name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

