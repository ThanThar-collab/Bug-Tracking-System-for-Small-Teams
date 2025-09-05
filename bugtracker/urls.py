
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from bugtracker_app import views
from django.conf import settings

# datetime model in python
from datetime import datetime

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bugtracker_app.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)