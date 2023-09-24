import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from mainapp.apps import MainappConfig

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url='mainapp/')),
    path("social_auth/", include("social_django.urls", namespace="social")),
    path('mainapp/', include('mainapp.urls', namespace=MainappConfig.name)),
    path('authapp/', include('authapp.urls', namespace='authapp'))
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

