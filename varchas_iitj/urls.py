"""varchas_iitj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from accounts.views import CustomLoginView, GoogleLogin
from django.conf.urls import handler404, handler500
from main.views import error_404, error_500
from django.conf.urls import url

urlpatterns = [
    path('webd', admin.site.urls, name='admin'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin/', include('adminportal.urls')),
    path('', include('main.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('account/', include('accounts.urls')),
    path('registration/', include('registration.urls')),
    path('events/', include('events.urls')),
    path('sponsors/', include('sponsors.urls')),
    path('accounts/', include('allauth.urls')),
    path('googlelogin/', GoogleLogin, name='googlelogin'),
    url('^', include('django.contrib.auth.urls')),
]

handler404 = error_404
handler500 = error_500
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
