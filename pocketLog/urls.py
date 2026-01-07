from django.contrib import admin
from django.urls import path, include

service_name = 'pocketLog'
urlpatterns = [
    path(f'{service_name}/admin/', admin.site.urls),
    # path('admin/', admin.site.urls),
]
