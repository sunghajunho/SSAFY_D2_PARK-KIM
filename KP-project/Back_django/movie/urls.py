"""
URL configuration for movie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# settings.py 아래에 넣고 runserver 중 출력 확인
from dj_rest_auth.registration.views import RegisterView
print('REGISTER VIEW SERIALIZER:', RegisterView.serializer_class)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('community/', include('community.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/',include('dj_rest_auth.urls')),
    path('accounts/signup/',include('dj_rest_auth.registration.urls')),
    path('api/recommend/', include('recommend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)