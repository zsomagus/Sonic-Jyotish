from django.db import models
from django.contrib.auth.models import User



class Elemzes(models.Model):
    vezetek_nev = models.CharField(max_length=50)
    kereszt_nev = models.CharField(max_length=50)
    datum = models.DateField()
    ido = models.TimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    ido_zona = models.CharField(max_length=50)
    nyari_idoszamitas = models.BooleanField(default=False)
    varga = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vezetek_nev} {self.kereszt_nev} – {self.datum}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    szuletesi_datum = models.DateField()
    horoszkop_kep = models.ImageField(upload_to='profil_kepek/', blank=True, null=True)
    bemutatkozas = models.TextField(blank=True)
    erdeklodes = models.CharField(max_length=200, blank=True)
    horoszkop_pdf = models.FileField(upload_to='profil_pdf/', blank=True, null=True)
    szuletesi_ido = models.TimeField(blank=True, null=True)
    szuletesi_hely = models.CharField(max_length=100, blank=True)
    fenykep = models.ImageField(upload_to='profil_kepek/', blank=True, null=True)
    nev = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} profilja"
# models.py


    def __str__(self):
        return f"{self.szerzo.username} – {self.letrehozva.strftime('%Y-%m-%d %H:%M')}"
    hold_nakshatra = models.CharField(max_length=50, blank=True)
    yantra_kep = models.ImageField(upload_to="poszt_yantrak/", blank=True, null=True)

# models.py

class KozossegiSzoba(models.Model):
    nev = models.CharField(max_length=100)
    leiras = models.TextField(blank=True)
    letrehozta = models.ForeignKey(User, on_delete=models.CASCADE)
    letrehozva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nev


class Poszt(models.Model):
    szerzo = models.ForeignKey(User, on_delete=models.CASCADE)
    szoba = models.ForeignKey(KozossegiSzoba, on_delete=models.SET_NULL, blank=True, null=True)
    szoveg = models.TextField(blank=True)
    kep = models.ImageField(upload_to="poszt_kepek/", blank=True, null=True)
    audio = models.FileField(upload_to="poszt_audio/", blank=True, null=True)
    pdf = models.FileField(upload_to="poszt_pdf/", blank=True, null=True)
    hold_nakshatra = models.CharField(max_length=50, blank=True)
    yantra_kep = models.ImageField(upload_to="poszt_yantrak/", blank=True, null=True)
    letrehozva = models.DateTimeField(auto_now_add=True)
# models.py

class Uzenet(models.Model):
    kuldo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kuldo_uzenetek")
    cimzett = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cimzett_uzenetek")
    szoveg = models.TextField()
    letrehozva = models.DateTimeField(auto_now_add=True)
    olvasott = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.kuldo.username} → {self.cimzett.username} ({self.letrehozva.strftime('%Y-%m-%d')})"
ai_valasz = models.TextField(blank=True, null=True)


class PadaFrekvencia(models.Model):
    bolygo = models.CharField(max_length=20)
    nakshatra = models.CharField(max_length=50)
    frekvencia = models.FloatField()

    class Meta:
        unique_together = ("bolygo", "nakshatra", "frekvencia")

    def __str__(self):
        return f"{self.bolygo} – {self.nakshatra} – {self.frekvencia} Hz"
class TelepulesKoordinata(models.Model):
    nev = models.CharField(max_length=100)
    orszag = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.nev} ({self.latitude}, {self.longitude})"
class FelhasznaloHoroszkop(models.Model):
    vezetek_nev = models.CharField(max_length=100)
    kereszt_nev = models.CharField(max_length=100)
    datum = models.DateField()
    ido = models.TimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    ido_zona = models.CharField(max_length=100)
    nyari_idoszamitas = models.BooleanField(default=False)
class NakshatraInfo(models.Model):
    nakshatra = models.CharField(max_length=50)
    tulajdonsag = models.TextField(blank=True)
    uralkodo = models.CharField(max_length=50, blank=True)
    mantra = models.CharField(max_length=100, blank=True)
    frekvencia = models.FloatField(blank=True, null=True)
class MantraMap(models.Model):
    jegy = models.IntegerField()
    bolygo = models.CharField(max_length=50)
    hz = models.FloatField()
    mantra = models.CharField(max_length=100)
class BolygoNakshatraMap(models.Model):
    bolygo = models.CharField(max_length=50)
    nakshatra1 = models.CharField(max_length=50)
    nakshatra2 = models.CharField(max_length=50)
    nakshatra3 = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bolygo}: {self.nakshatra1}, {self.nakshatra2}, {self.nakshatra3}"
class OrszagKoordinata(models.Model):
    regiokategoria = models.CharField(max_length=100)  # pl. 'Európa', 'Ázsia', stb.
    allam_terulet = models.CharField(max_length=100)
    fovaros = models.CharField(max_length=100)
    szelesseg = models.FloatField()
    hosszusag = models.FloatField()

    def __str__(self):
        return f"{self.allam_terulet} ({self.regiokategoria})"
class KulcsszoValasz(models.Model):
    kulcsszo = models.CharField(max_length=100)
    valasz_szoveg = models.TextField()
    ajanlott_mantra = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.kulcsszo} → {self.ajanlott_mantra}"
class PurushartaMap(models.Model):
    haz = models.IntegerField()
    purusharta = models.CharField(max_length=50)

    def __str__(self):
        return f"Ház {self.haz} → {self.purusharta}"
class VargaFaktor(models.Model):
    betujel = models.CharField(max_length=5)
    reszhoroszkop = models.CharField(max_length=50)
    oszto = models.FloatField()

    def __str__(self):
        return f"{self.betujel} – {self.reszhoroszkop}"
class TithiAjanlas(models.Model):
    szam = models.IntegerField()
    tipus = models.CharField(max_length=50)
    nev = models.CharField(max_length=100)
    jelentes = models.TextField()
    napi_ajanlas = models.TextField()

    def __str__(self):
        return f"{self.szam}. {self.nev} – {self.tipus}"
class PlanetID(models.Model):
    szam = models.IntegerField()
    napja = models.CharField(max_length=20)
    bolygo_kod = models.CharField(max_length=50)
    efemerida = models.CharField(max_length=50)
    bolygo_nev = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bolygo_nev} – {self.szam}"
class PlanetAbbreviation(models.Model):
    bolygo = models.CharField(max_length=50)
    rovidites = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.bolygo} = {self.rovidites}"
class Nakshatra(models.Model):
    szam = models.IntegerField()
    nev = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.szam}. {self.nev}"
class NakshatraInfo(models.Model):
    nakshatra = models.CharField(max_length=50)
    ura = models.CharField(max_length=50)
    tulajdonsag = models.TextField(blank=True)
    mantra = models.CharField(max_length=100, blank=True)
    frekvencia = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.nakshatra} – {self.ura}"
class JegyUralkodo(models.Model):
    jegy = models.CharField(max_length=50)
    ura = models.CharField(max_length=50)
    hz = models.FloatField()

    def __str__(self):
        return f"{self.jegy} → {self.ura} ({self.hz} Hz)"
class HousePosition(models.Model):
    jegy_szam = models.IntegerField()
    x_koordinata = models.FloatField()
    y_koordinata = models.FloatField()
    jegy_nev = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.jegy_szam} – {self.jegy_nev}"
class GrahaTranzit(models.Model):
    jegy = models.CharField(max_length=50)
    asc_fugg = models.CharField(max_length=50)
    bolygo = models.CharField(max_length=50)
    hang = models.CharField(max_length=100)
    hz = models.FloatField()

    def __str__(self):
        return f"{self.bolygo} @ {self.jegy} [{self.asc_fugg}] – {self.hang} ({self.hz} Hz)"
class Jegy(models.Model):
    nev = models.CharField(max_length=50)
    tulajdonsagok = models.TextField(blank=True)
    uralkodo = models.CharField(max_length=50)

    def __str__(self):
        return self.nev
class Haz(models.Model):
    szam = models.IntegerField()
    tulajdonsagok = models.TextField(blank=True)
    uralkodo_bolygo = models.CharField(max_length=50)
    purusharta = models.CharField(max_length=50)

    def __str__(self):
        return f"Ház {self.szam}"
class Bolygo(models.Model):
    nev = models.CharField(max_length=50)
    tulajdonsagok = models.TextField(blank=True)
    szamok = models.CharField(max_length=50)
    napok = models.CharField(max_length=50)
    noveny = models.CharField(max_length=100)
    kristaly = models.CharField(max_length=100)
    szimbolum = models.CharField(max_length=100)

    def __str__(self):
        return self.nev
class NakshatraPada(models.Model):
    nakshatra = models.CharField(max_length=50)
    tulajdonsagok = models.TextField(blank=True)
    pada_dharma = models.CharField(max_length=100)
    pada_artha = models.CharField(max_length=100)
    pada_kama = models.CharField(max_length=100)
    pada_moksha = models.CharField(max_length=100)

    def __str__(self):
        return self.nakshatra
class CharaKaraka(models.Model):
    karaka = models.CharField(max_length=50)
    tulajdonsagok = models.TextField(blank=True)

    def __str__(self):
        return self.karaka
class VargaInfo(models.Model):
    nev = models.CharField(max_length=10)  # D jelzés pl. D9
    hanyad = models.CharField(max_length=20)
    mire_hasznaljuk = models.TextField()
    hany_fok_jegy = models.FloatField()

    def __str__(self):
        return self.nev
class Elem(models.Model):
    nev = models.CharField(max_length=20)

class ElemTulajdonsag(models.Model):
    elem = models.ForeignKey(Elem, on_delete=models.CASCADE)
    tulajdonsag = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.elem.nev}: {self.tulajdonsag}"
class Csakra(models.Model):
    nev = models.CharField(max_length=50)
    mirigy = models.CharField(max_length=100)
    szin = models.CharField(max_length=50)
    elem = models.CharField(max_length=50)
    bolygo = models.CharField(max_length=50)
    tulajdonsag = models.TextField(blank=True)

    def __str__(self):
        return self.nev
