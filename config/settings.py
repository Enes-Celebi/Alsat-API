import os
import environ

env = environ.Env()

environ.Env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

DATABASES = {
    'default': env.db('DATABASE_URL')
}

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ROOT_URLCONF = 'config.urls'

INSTALLED_APPS = [
    'app',  
    'django.contrib.sessions',  
    'django.contrib.messages',  
    'django.contrib.staticfiles', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',  
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'  

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
