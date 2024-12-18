import os
import sys
import environ

env = environ.Env()

environ.Env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
