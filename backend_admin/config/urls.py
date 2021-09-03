from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("movies.api.urls")),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [re_path(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
