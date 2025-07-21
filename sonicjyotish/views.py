from .models import Elemzes


def index_view(request):
    if request.method == "POST":
        # 1️⃣ Ha pontszám-értékeléses POST
        if all(q in request.POST for q in ['q1', 'q2', 'q3', 'q4']):
            try:
                pontszam = sum(int(request.POST.get(q, 0)) for q in ['q1', 'q2', 'q3', 'q4'])
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
    return render(request, "index.html", {
        "vargak": ["D1 (Rashi)", "D2 (Hora)", "D3 (Drekkana)", "D9 (Navamsha)"]
    })
