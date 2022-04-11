import debug_toolbar

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DenzelProject.mainApp.urlsMain')),
    path('profile/', include('DenzelProject.profileApp.urlsProfile')),
    path('posts/', include('DenzelProject.blogPost.urlsPost')),
    # path('__debug__/', include(debug_toolbar.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

import DenzelProject.signals
