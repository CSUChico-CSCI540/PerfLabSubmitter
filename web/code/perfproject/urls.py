"""perfproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

import os.path
site_media = os.path.join(os.path.dirname(__file__), 'site_media')


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media}),
    url(r'^$', 'perfapp.views.home'),
    url(r'^init$','perfapp.views.init'),
    url(r'^server$','perfapp.views.getServer'),
    url(r'^wupdate$','perfapp.views.wupdate'),
    url(r'^grade$','perfapp.views.grade'),
]
