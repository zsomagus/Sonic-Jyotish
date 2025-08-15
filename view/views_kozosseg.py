from django.contrib.auth.decorators import login_required
from sonicjyotish.forms import ProfilSzerkesztoForm
from django.db.models import Q
from sonicjyotish.models import UserProfile
from utils.sj import get_nakshatra_for_now, generate_yantra
from sonicjyotish.forms import PosztForm
from sonicjyotish.models import Poszt
from utils.sj import get_current_moon_nakshatra
from utils.sj import get_current_tithi
from datetime import datetime
from sonicjyotish.forms import UzenetForm
from sonicjyotish.models import Uzenet
import views_astro
import sj
import postgresql
import belepteto_views
def regisztracio_view(request):
    if not request.session.get('belepve'):
        return redirect('belepteto_view')
    # ...a többi rész ugyanaz marad
    if request.method == "POST":
        form = RegisztraciosForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = user.userprofile
            profile.szuletesi_datum = form.cleaned_data["szuletesi_datum"]
            profile.bemutatkozas = form.cleaned_data["bemutatkozas"]
            profile.erdeklodes = form.cleaned_data["erdeklodes"]
            profile.save()

            login(request, user)
            return redirect("profil")  # vagy egyedi dashboard nézet
    else:
        form = RegisztraciosForm()
    return render(request, "regisztracio.html", {"form": form})
...
profile.save()

# Automatikus horoszkópgenerálás
generate_horoszkop_for_user(user)

login(request, user)
return redirect("profil")

@login_required
def profil_szerkeszto_view(request):
    profil = request.user.userprofile
    if request.method == 'POST':
        form = ProfilSzerkesztoForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('profil')  # vagy bárhová vissza akarod vinni
    else:
        form = ProfilSzerkesztoForm(instance=profil)
    return render(request, 'profil_szerkesztes.html', {'form': form})

def kozosseg_list_view(request):
    keres = request.GET.get("keres", "")
    if keres:
        profilok = UserProfile.objects.filter(
            Q(erdeklodes__icontains=keres) |
            Q(bemutatkozas__icontains=keres)
        ).select_related("user")
    else:
        profilok = UserProfile.objects.all().select_related("user")
    return render(request, "kozosseg.html", {
        "profilok": profilok,
        "keres": keres
    })

poszt = form.save(commit=False)
poszt.szerzo = request.user
poszt.hold_nakshatra = get_nakshatra_for_now()
poszt.yantra_kep = generate_yantra(user=poszt.szerzo)
poszt.save()

@login_required
def posztok_view(request):
    if request.method == "POST":
        form = PosztForm(request.POST, request.FILES)
        if form.is_valid():
            poszt = form.save(commit=False)
            poszt.szerzo = request.user
            poszt.save()
            return redirect("posztok")  # név egyezzen az urls.py-ben
    else:
        form = PosztForm()

    posztok = Poszt.objects.all().order_by("-letrehozva")
    return render(request, "posztok.html", {
        "form": form,
        "posztok": posztok
    })

if form.is_valid():
    poszt = form.save(commit=False)
    poszt.szerzo = request.user
    poszt.hold_nakshatra = get_current_moon_nakshatra()
    poszt.save()


now = datetime.utcnow()
jd = swe.julday(now.year, now.month, now.day,
                now.hour + now.minute/60 + now.second/3600)

tithi = get_current_tithi(jd)
poszt.tithi_szam = tithi
poszt.yantra_kep.name = f"yantra_tithi/{tithi}.png"
# views.py

@login_required
def uj_szoba_view(request):
    if request.method == "POST":
        form = SzobaForm(request.POST)
        if form.is_valid():
            szoba = form.save(commit=False)
            szoba.letrehozta = request.user
            szoba.save()
            return redirect("kozossegi_szobak")
    else:
        form = SzobaForm()
    return render(request, "uj_szoba.html", {"form": form})


def szobalista_view(request):
    szobak = KozossegiSzoba.objects.all().order_by("-letrehozva")
    return render(request, "szobak.html", {"szobak": szobak})
# views.py


@login_required
def uzenet_kuldes_view(request):
    if request.method == "POST":
        form = UzenetForm(request.POST)
        if form.is_valid():
            uzenet = form.save(commit=False)
            uzenet.kuldo = request.user
            uzenet.save()
            return redirect("bejovo_uzenetek")
    else:
        form = UzenetForm()
    return render(request, "uzenet_kuldes.html", {"form": form})
@login_required
def bejovo_uzenetek_view(request):
    uzenetek = Uzenet.objects.filter(cimzett=request.user).order_by("-letrehozva")
    return render(request, "bejovo_uzenetek.html", {"uzenetek": uzenetek})
def idovonal_view(request):
    posztok = Poszt.objects.select_related("szerzo", "szoba").order_by("-letrehozva")
    return render(request, "idovonal.html", {"posztok": posztok})
def astroai_chat_view(request):
    if request.method == "POST":
        kerdes = request.POST.get("kerdes")
        valasz = generate_astro_response(kerdes)
        return render(request, "astroai.html", {"kerdes": kerdes, "valasz": valasz})
    return render(request, "astroai.html")
def generate_astro_response(kerdes):
    if "punarvasu" in kerdes.lower():
        return "Punarvasu a Jupiter uralma alatt áll, és az 'om' mantra rezonál vele. Ez a tudás, belső megértés ideje."
    # további keresések, regex, NLP kiegészítéssel
audio_path = poszt.audio.path
felismert_szoveg = felismer_szoveget_audio_fajlbol(audio_path)
poszt.szoveg = felismert_szoveg
valasz = generate_astro_response(felismert_szoveg)
poszt.ai_valasz = valasz  # ezt te mentheted akár külön mezőként


