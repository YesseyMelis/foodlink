"""foodlink_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, SpectacularAPIView

patterns = [
    path('', include('foodlink_back.apps.authentication.urls', namespace='authentication')),
    path('orders/', include('foodlink_back.apps.order.urls', namespace='orders')),
    path('core/', include('foodlink_back.apps.core.urls', namespace='address')),
    path('common/', include('foodlink_back.apps.common.urls', namespace='common')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(patterns)),
    url(r'^schema/$', SpectacularAPIView.as_view(), name='schema'),
    url(r'^swagger/$', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    url(r'^redoc/$', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
