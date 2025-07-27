from django.urls import path
from .views import index_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.urls import path
from .views import index_view
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', index_view, name='index'),  # kezdőoldal űrlappal
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('accounts/', include('accounts.urls')),
]
path('', include('asztroapp.urls')),



urlpatterns = [
    path("eloregisztracio/", views.eloregisztracio_view, name="eloregisztracio"),
    path("regisztracio/", views.regisztracio_view, name="regisztracio_view"),
]


generate_horoszkop_for_user(user)  # Te írod meg, és hozzárendeli a képet

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
path("profil/szerkesztes/", profil_szerkeszto_view, name="profil_szerkesztes"),
path("kozosseg/", kozosseg_list_view, name="kozosseg"),
path("posztok/", posztok_view, name="posztok"),
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
path("szobak/", szobalista_view, name="kozossegi_szobak"),
path("szobak/uj/", uj_szoba_view, name="uj_szoba"),
path("uzenet/kuldes/", uzenet_kuldes_view, name="uzenet_kuldes"),
path("uzenet/bejovo/", bejovo_uzenetek_view, name="bejovo_uzenetek"),
