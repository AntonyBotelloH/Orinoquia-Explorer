"""
Django settings for app project (Orinoquia Explorer).
Configurado para desarrollo local y despliegue en cPanel (Passenger / LiteSpeed)
bajo el subdirectorio /orinoquiaxp/ en bbingenieros.online
"""

import os
from pathlib import Path
import pymysql
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar .env si existe (local o en producción) con override=True para evitar cruce de variables de LiteSpeed
load_dotenv(BASE_DIR / '.env', override=True)

# Parche para que Django use PyMySQL en lugar de mysqlclient en cPanel
pymysql.install_as_MySQLdb()
pymysql.version_info = (2, 2, 3, 'final', 0)

# Parche para compatibilidad con la versión de MariaDB/MySQL en cPanel
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None
except Exception:
    pass

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-9=%(k0^@7)0u(&5gk-ji=c6a#el0(n)z_wcszymlvz6c_5qf24')

# DEBUG: False en producción si la variable DEBUG se define como False
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

env_allowed_hosts = os.getenv('ALLOWED_HOSTS')
if env_allowed_hosts:
    ALLOWED_HOSTS = [h.strip() for h in env_allowed_hosts.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = ['bbingenieros.online', 'www.bbingenieros.online', 'localhost', '127.0.0.1', '*']

env_csrf = os.getenv('CSRF_TRUSTED_ORIGINS')
if env_csrf:
    CSRF_TRUSTED_ORIGINS = [c.strip() for c in env_csrf.split(',') if c.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://bbingenieros.online',
        'https://www.bbingenieros.online',
        'http://bbingenieros.online',
        'http://www.bbingenieros.online',
    ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'experiencias',
    'turismo',
    'reservas',
    'aliados', 
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_USER_MODEL = 'usuarios.Usuario'

AUTHENTICATION_BACKENDS = [
    'usuarios.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'turismo.context_processors.clima_context',
            ],
            'builtins': [
                'turismo.templatetags.moneda',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# Si se provee DB_ENGINE=django.db.backends.mysql o DB_NAME en el entorno, usa MySQL
DB_ENGINE = os.getenv('DB_ENGINE', '')
if DB_ENGINE == 'django.db.backends.mysql' or os.getenv('DB_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'bbingeni_orinoquia_xp'),
            'USER': os.getenv('DB_USER', 'bbingeni_orinoquia_xp_user'),
            'PASSWORD': os.getenv('DB_PASSWORD', '.GdKf8?NY~!p!%Nd'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Subdirectorio / Prefijo de la App en Producción (ej: /orinoquiaxp)
FORCE_SCRIPT_NAME = os.getenv('FORCE_SCRIPT_NAME', None)

# Static files (CSS, JavaScript, Images)
STATIC_URL = os.getenv('STATIC_URL', '/static/')
if FORCE_SCRIPT_NAME and STATIC_URL.startswith('/') and not STATIC_URL.startswith(FORCE_SCRIPT_NAME):
    STATIC_URL = FORCE_SCRIPT_NAME + STATIC_URL

env_static_root = os.getenv('STATIC_ROOT')
STATIC_ROOT = Path(env_static_root) if env_static_root else (BASE_DIR / "staticfiles")
STATICFILES_DIRS = [BASE_DIR / "static"]

# Configuración WhiteNoise para servir estáticos eficientemente en producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
if FORCE_SCRIPT_NAME and MEDIA_URL.startswith('/') and not MEDIA_URL.startswith(FORCE_SCRIPT_NAME):
    MEDIA_URL = FORCE_SCRIPT_NAME + MEDIA_URL

env_media_root = os.getenv('MEDIA_ROOT')
MEDIA_ROOT = Path(env_media_root) if env_media_root else (BASE_DIR / "media")

# Email
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# Login
LOGIN_URL = os.getenv('LOGIN_URL', 'login')
LOGIN_REDIRECT_URL = os.getenv('LOGIN_REDIRECT_URL', 'index_usuario')
LOGOUT_REDIRECT_URL = os.getenv('LOGOUT_REDIRECT_URL', 'login')
