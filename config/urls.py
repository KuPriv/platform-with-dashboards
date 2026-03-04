import debug_toolbar
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/datasets/", include("apps.datasets.urls")),
]
