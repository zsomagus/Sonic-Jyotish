from sonicjyotish.models import Elemzes, UserProfile
from utils import sj
from django.shortcuts import render, redirect
from sonicjyotish.forms import RegisztraciosForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from sonicjyotish.models import KozossegiSzoba
from sonicjyotish.models import Poszt
from sonicjyotish.models import KozossegiSzoba
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")

@login_required
def letolt_pdf_view(request):
    profil = request.user.userprofile
    if profil.horoszkop_pdf:
        return redirect(profil.horoszkop_pdf.url)
    return render(request, "profil_pdf.html", {"hiba": True})

def idovonal_view(request):
    posztok = Poszt.objects.all().order_by("-letrehozva")
    return render(request, "idovonal.html", {"posztok": posztok})

@login_required
def bejovo_uzenetek_view(request):
    uzenetek = Uzenet.objects.filter(cimzett=request.user).order_by("-letrehozva")
    return render(request, "bejovo_uzenetek.html", {"uzenetek": uzenetek})

@login_required
def uzenet_kuldes_view(request):
    if request.method == "POST":
        cimzett_id = request.POST.get("cimzett_id")
        szoveg = request.POST.get("szoveg")
        try:
            cimzett = User.objects.get(id=cimzett_id)
            Uzenet.objects.create(kuldo=request.user, cimzett=cimzett, szoveg=szoveg)
            return redirect("bejovo_uzenetek")
        except User.DoesNotExist:
            pass
    felhasznalok = User.objects.exclude(id=request.user.id)
    return render(request, "uzenet_kuldes.html", {"felhasznalok": felhasznalok})

def szobalista_view(request):
    szobak = KozossegiSzoba.objects.all().order_by("-letrehozva")
    return render(request, "szobak.html", {"szobak": szobak})

def index_view(request):
    if request.method == "POST":
        # 1️⃣ Ha pontszám-értékeléses POST
        if all(q in request.POST for q in ['q1', 'q2', 'q3', 'q4', 'q5']):
            try:
                pontszam = sum(int(request.POST.get(q, 0)) for q in ['q1', 'q2', 'q3', 'q4', 'q5'])
            except ValueError:
                pontszam = 0
            if pontszam >= 10:
                return render(request, "kapunyit.html")
            else:
                hiba = "Sajnos még nem elegendő a belépéshez!"
                return render(request, "index.html", {"hiba": hiba})

        # 2️⃣ Ha Elemzes típusú POST (az elemzés mezői szerepelnek)
        elif "vezetek_nev" in request.POST and "kereszt_nev" in request.POST:
            nev = request.POST.get("vezetek_nev")
            kereszt = request.POST.get("kereszt_nev")
            datum = request.POST.get("datum")
            ido = request.POST.get("ido")
            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")
            ido_zona = request.POST.get("ido_zona")
            nyari = request.POST.get("nyari_idoszamitas") == "igen"
            varga = request.POST.get("varga")

            elemzes = Elemzes.objects.create(
                vezetek_nev=nev,
                kereszt_nev=kereszt,
                datum=datum,
                ido=ido,
                latitude=latitude,
                longitude=longitude,
                ido_zona=ido_zona,
                nyari_idoszamitas=nyari,
                varga=varga
            )

            return render(request, "eredmeny.html", {
                "nev": f"{nev} {kereszt}",
                "napjegy": "...",
                "aszcendens": "...",
                "hang_url": "/static/hangok/valami.wav"
            })

    # 3️⃣ GET-kérés — sima kezdőoldal
    return render(request, "index.html") 
    vargak=varga,
    {
        "vargak": ["D1 (Rashi)", "D2 (Hora)", "D3 (Drekkana)", "D9 (Navamsha)"]
    }

def eloregisztracio_view(request):
    pontszam = None
    if request.method == 'POST':
        try:
            pontszam = sum(int(request.POST.get(q, 0)) for q in ['q1', 'q2', 'q3', 'q4', 'q5'])
        except ValueError:
            pontszam = 0
        return render(request, 'eloregisztracio.html', {'pontszam': pontszam})
    return render(request, 'eloregisztracio.html', {})

def regisztracio_view(request):
    if request.method == "POST":
        felhasznalo_form = FelhasznaloForm(request.POST)
        profil_form = ProfilForm(request.POST, request.FILES)
        if felhasznalo_form.is_valid() and profil_form.is_valid():
            user = felhasznalo_form.save()  # tartalmazza username, email, jelszó, stb.
            profile = profil_form.save(commit=False)
            profile.user = user
            profile.save()
            generate_horoszkop_for_user(user)
            login(request, user)
            return redirect('profil')
    else:
        felhasznalo_form = FelhasznaloForm()
        profil_form = ProfilForm()

    return render(request, 'regisztracio.html', {
        'felhasznalo_form': felhasznalo_form,
        'profil_form': profil_form
    })
def generate_horoszkop_for_user(user):
    profil = Profil.objects.get(user=user)
    # itt jönne a számítás a születési adatok alapján
    # pl. horoszkóp generálás, kép mentése

    image_path = create_chart_image(profil.születési_dátum, profil.születési_idő, profil.szélesség, profil.hosszúság)
    profil.horoszkop_kep = image_path  # ez lehet ImageField vagy fájlútvonal
    profil.save()

def profil_szerkeszto_view(request):
    # Példa: profil szerkesztő oldal megjelenítése
    return render(request, "profil_szerkesztes.html")

def kozosseg_list_view(request):
    szobak = KozossegiSzoba.objects.all()
    return render(request, "kozosseg.html", {"szobak": szobak})

def posztok_view(request):
    posztok = Poszt.objects.all().order_by("-letrehozva")
    return render(request, "posztok.html", {"posztok": posztok})
@login_required
def uj_szoba_view(request):
    if request.method == "POST":
        nev = request.POST.get("nev")
        leiras = request.POST.get("leiras")
        if nev:
            KozossegiSzoba.objects.create(
                nev=nev,
                leiras=leiras,
                letrehozta=request.user
            )
            return redirect("kozossegi_szobak")
    return render(request, "uj_szoba.html")
def index(request):
    pontszam = None
    if request.method == "POST":
        válaszok = [
            int(request.POST.get("q1", 0)),
            int(request.POST.get("q2", 0)),
            int(request.POST.get("q3", 0)),
            int(request.POST.get("q4", 0)),
            int(request.POST.get("q5", 0)),
        ]
        pontszam = sum(válaszok)
    return render(request, "eloregisztracio.html", {"pontszam": pontszam})

def astro_main_view(request):
    return render(request, 'astro/index.html')
if not request.session.get('belepve'):
    return redirect('belepteto_view')


def belepteto_view(request):
    pontszam = None
    if request.method == 'POST':
        try:
            pontszam = sum(int(request.POST.get(q, 0)) for q in ['q1', 'q2', 'q3', 'q4'])
        except ValueError:
            pontszam = 0
        if pontszam >= 10:
            request.session['belepve'] = True  # vagy mentheted a user profilba
            return redirect('regisztracio_view')
        else:
            return render(request, 'belepteto.html', {'pontszam': pontszam, 'hiba': "Még nem ébredtél..."})
    return render(request, 'belepteto.html')
