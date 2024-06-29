from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from config import settings

urlpatterns = [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
