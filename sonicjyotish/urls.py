from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('eloregisztracio/', views.eloregisztracio_view, name='eloregisztracio'),
    path('regisztracio/', views.regisztracio_view, name='regisztracio_view'),
    path('astro/', views.astro_main_view, name='astro_main'),
    path("profil/szerkesztes/", views.profil_szerkeszto_view, name="profil_szerkesztes"),
    path("kozosseg/", views.kozosseg_list_view, name="kozosseg"),
    path("posztok/", views.posztok_view, name="posztok"),
    path("szobak/", views.szobalista_view, name="kozossegi_szobak"),
    path("szobak/uj/", views.uj_szoba_view, name="uj_szoba"),
    path("uzenet/kuldes/", views.uzenet_kuldes_view, name="uzenet_kuldes"),
    path("uzenet/bejovo/", views.bejovo_uzenetek_view, name="bejovo_uzenetek"),
]

# statikus és média fájlok kiszolgálása fejlesztéskor
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)