from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("home/", views.home, name="home"),
    path("konsep-singkat/", views.konsep_singkat, name="konsep-singkat"),
    path("how-to-use/", views.how_to_use, name="how-to-use"),
    path("about-us/", views.about_us, name="about-us"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)