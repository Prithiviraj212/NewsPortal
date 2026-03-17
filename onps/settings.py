from pathlib import Path
import os

# ------------------ BASE DIR ------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------ SECRET KEY ------------------
SECRET_KEY = 'django-insecure-vsxlkoda(-#mhn81#)vd(^5fojxq6hr0vd-$siv3z9!5t@z$ai'

# ------------------ DEBUG & HOSTS ------------------
DEBUG = True  # Change to False in production
ALLOWED_HOSTS = [
    'newsportal-u0as.onrender.com',  # Render URL
    '127.0.0.1',
    'localhost'
]

# ------------------ INSTALLED APPS ------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'newsapp',  # Your app
]

# ------------------ MIDDLEWARE ------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------ URLS ------------------
ROOT_URLCONF = 'onps.urls'

# ------------------ TEMPLATES ------------------
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
                'newsapp.context_processors.category_processor',
                'newsapp.context_processors.aboutus',
            ],
        },
    },
]

# ------------------ WSGI ------------------
WSGI_APPLICATION = 'onps.wsgi.application'

# ------------------ DATABASE ------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newspythondb',  # Change if Render MySQL used
        'USER': 'root',
        'PASSWORD': '',           # Change password in production
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# ------------------ PASSWORD VALIDATORS ------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------ LANGUAGE & TIME ------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------ STATIC FILES ------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ------------------ MEDIA FILES ------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------ DEFAULT AUTO FIELD ------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'newsapp.CustomUser'

# ------------------ SESSIONS ------------------
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ------------------ CSRF & LOGIN ------------------
CSRF_COOKIE_SECURE = False
LOGIN_URL = '/login/'

# ------------------ DEVELOPMENT HELPERS ------------------
if DEBUG:
    import mimetypes
    mimetypes.add_type("text/css", ".css", True)