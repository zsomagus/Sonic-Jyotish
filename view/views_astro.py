from django.shortcuts import render
from .models import Elemzes
from utils import sj
from django.http import JsonResponse
from .models import TelepulesKoordinata
from django.shortcuts import render, redirect
from .forms import RegisztraciosForm
from .models import UserProfile
from django.contrib.auth import login
import views_kozosseg
import postgresql

def index_view(request):
    if request.method == "POST":
        nev = request.POST.get("vezetek_nev")
        kereszt = request.POST.get("kereszt_nev")
        datum = request.POST.get("datum")
        ido = request.POST.get("ido")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        ido_zona = request.POST.get("ido_zona")
        nyari = request.POST.get("nyari_idoszamitas") == "igen"
        varga = request.POST.get("varga")

        # Mentés adatbázisba
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

        # Mentett fájlnevek
        horoszkop_filename = f"{nev.lower()}_{kereszt.lower()}_horoszkop.png"
        hang_filename = f"{nev.lower()}_{kereszt.lower()}_{varga.lower()}.wav"
        pdf_filename = f"{nev.lower()}_{kereszt.lower()}_kotta_output.pdf"

        # Ha még nincs napjegy/aszcendens kiszámítva:
        napjegy = "Kos"
        aszcendens = "Oroszlán"

        return render(request, "index.html", {
            "nev": f"{nev} {kereszt}",
            "napjegy": napjegy,
            "aszcendens": aszcendens,
            "hang_url": f"hangok/{hang_filename}",
            "pdf_url": f"kottak/{pdf_filename}",
            "kep_url": f"horoszkopok/{horoszkop_filename}",
            "vargak": [
                "D1 (Rashi)", "D2 (Hora)", "D3 (Drekkana)", "D9 (Navamsha)"
            ]
        })

    return render(request, "index.html", {
        "vargak": [
            "D1 (Rashi)", "D2 (Hora)", "D3 (Drekkana)", "D9 (Navamsha)"
        ]
    })


def get_koordinatak(request):
    varos = request.GET.get('varos', '')
    try:
        entry = TelepulesKoordinata.objects.get(nev__iexact=varos)
        return JsonResponse({
            "latitude": entry.latitude,
            "longitude": entry.longitude
        })
    except TelepulesKoordinata.DoesNotExist:
        return JsonResponse({"error": "Nincs találat"}, status=404)

