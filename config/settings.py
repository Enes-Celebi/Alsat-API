import os
import environ

env = environ.Env()

environ.Env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

DATABASES = {
    'default': env.db('DATABASE_URL')  
}

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

