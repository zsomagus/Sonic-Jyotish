from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from sonicjyotish.models import UserProfile
from sonicjyotish.models import Poszt
from django import forms
from django.contrib.auth.models import User
from sonicjyotish.models import UserProfile
from sonicjyotish.models import KozossegiSzoba
from sonicjyotish.models import Uzenet
from .models import Profil

class FelhasznaloForm(forms.ModelForm):
    # User mezőket is itt definiálod
    first_name = forms.CharField(label="Keresztnév")
    last_name = forms.CharField(label="Vezetéknév")
    email = forms.EmailField(label="Email")

    class Meta:
        model = UserProfile
        fields = [
            'szuletesi_datum',
            'szuletesi_ido',
            'szuletesi_hely',
            'bemutatkozas',
            'erdeklodes',
            'fenykep',
        ]

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = [
            'nev', 'szuletesi_datum', 'szuletesi_ido', 'szuletesi_hely',
            'szelesseg', 'hosszusag', 'bemutatkozas', 'fenykep'
        ]
        widgets = {
            'szuletesi_datum': forms.DateInput(attrs={'type': 'date'}),
            'szuletesi_ido': forms.TimeInput(attrs={'type': 'time'}),
        }

class RegisztracioForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['születési_dátum', 'születési_idő', 'szélesség', 'hosszúság']
        widgets = {
            'születési_dátum': forms.DateInput(attrs={'type': 'date'}),
            'születési_idő': forms.TimeInput(attrs={'type': 'time'}),
        }
        
        from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FelhasznaloForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email címed")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Felhasználónév',
            'password1': 'Jelszó',
            'password2': 'Jelszó megerősítése',
        }

CreationForm):
    email = forms.EmailField(required=True)
    szuletesi_datum = forms.DateField(label="Születési dátum", widget=forms.DateInput(attrs={"type": "date"}))
    bemutatkozas = forms.CharField(widget=forms.Textarea, required=False)
    erdeklodes = forms.CharField(label="Érdeklődési kör", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "szuletesi_datum", "bemutatkozas", "erdeklodes")

class ProfilSzerkesztoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['szuletesi_datum', 'bemutatkozas', 'erdeklodes', 'horoszkop_kep']
        widgets = {
            'szuletesi_datum': forms.DateInput(attrs={"type": "date"}),
            'bemutatkozas': forms.Textarea(attrs={"rows": 4}),
        }
# forms.py


# forms.py

# forms.py

class SzobaForm(forms.ModelForm):
    class Meta:
        model = KozossegiSzoba
        fields = ['nev', 'leiras']
class PosztForm(forms.ModelForm):
    class Meta:
        model = Poszt
        fields = ['szoba', 'szoveg', 'kep', 'audio', 'pdf']
# forms.py

class UzenetForm(forms.ModelForm):
    class Meta:
        model = Uzenet
        fields = ["cimzett", "szoveg"]
