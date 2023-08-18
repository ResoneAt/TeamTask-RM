from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('api/', include('api.urls', namespace='api')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api-auth/', include('rest_framework.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

