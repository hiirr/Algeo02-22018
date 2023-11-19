"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from cbir import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("home/", views.home, name="home"),
    path("konsep-singkat/", views.konsep_singkat, name="konsep-singkat"),
    path("how-to-use/", views.how_to_use, name="how-to-use"),
    path("about-us/", views.about_us, name="about-us"),
    path("upload_search/", views.upload_search, name="upload_search"),
    path("search_cbir/", views.search_cbir, name="search_cbir"),
    path("upload_dataset/", views.upload_dataset, name="upload_dataset"),
    path("refresh/", views.refresh, name="refresh"),
    path("admin/", admin.site.urls)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)