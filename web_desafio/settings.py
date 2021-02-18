import os
from os import path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# ATENÇÃO: Essa chave deve ser escondida para um deploy em produção
SECRET_KEY = 'k0ujs9pcw+7qohwas!o7_ept20$c@$)-b=qco8sgviy_f)((bc'

# ATENÇÃO: Não utilizar DEBUG = True em um deploy de produção
DEBUG = True

# ATENÇÃO: Nunca permitir além dos hosts necessarios
ALLOWED_HOSTS = ['ec2-18-223-125-126.us-east-2.compute.amazonaws.com', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'core',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_desafio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_desafio.wsgi.application'


# Banco de dados SQLite3 para rodar em maquina local sem Docker
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Banco de dados PostgreSQL hospedado na Amazon Web Service (RDS)
# Essas informações devem ser escondidas para um deploy em produção
DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'pastel123',
        'HOST': 'pasteldb.cxnr9fxthwtv.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1000,
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

LANGUAGE_CODE = 'pt-br'  # Lingua padrão do servidor web

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Arquivos estaticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    path.join(BASE_DIR, 'static'),
]
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Arquivos dos usuarios
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Pagina de redirecionamento
LOGIN_REDIRECT_URL='/afterlogin'

# Informações SMTP e de login do e-mail da empresa
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Host do servidor do e-mail
EMAIL_USE_TLS = True
EMAIL_PORT = 587  # Porta do servidor do e-mail
EMAIL_HOST_USER = 'desafio.caio.smn@gmail.com'  # E-mail (para enviar e-mail)
EMAIL_HOST_PASSWORD = '72DJXqT5AbXEJc'  # Senha do e-mail da empresa
EMAIL_RECEIVING_USER = ['desafio.caio.smn@gmail.com']  # E-mail (para receber e-mail)
