from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #includeは他のURLconfへの参照が可能。
    path("schedule/", include("schedule.urls")),
    path("", include("schedule.urls")),
    path('admin/', admin.site.urls),
]
