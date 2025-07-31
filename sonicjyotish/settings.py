import os
from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ALLOWED_HOSTS = ['sonic-jyotish.onrender.com', '127.0.0.1', 'localhost']
DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Production esetén:
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
SECRET_KEY = os.environ.get("SECRET_KEY", "!#582am_6hyb$7m$^yisa2cc!7-h(4rv#^_#^(l)j52m1^x+$d")

# Ha Whitenoise-t használsz (Renderen: igen)
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ⬅️ kell az adminhoz
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ⬅️ kell az adminhoz
    'django.contrib.messages.middleware.MessageMiddleware',  # ⬅️ kell az adminhoz
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    # ... a többi
]

# Opcionálisan:
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'sonicjyotish.urls'  # ha a urls.py a sonicjyotish mappában van
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',  # ✅ ennek itt kell lennie!
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sonicjyotish.apps.SonicjyotishConfig',  # ← saját appod neve
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
