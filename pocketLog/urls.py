from django.contrib import admin
from django.urls import path, include

service_name = 'pocket-log'
urlpatterns = [
    path(f'{service_name}/admin/', admin.site.urls),
    path(f'{service_name}/accounts/', include('accounts.urls')),
]

# Admin
admin.site.site_header = "Pocket Log"
admin.site.index_title = "Pocket Log"
admin.site.site_title = "Pocket Log"