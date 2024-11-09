# my_project/settings/__init__.py
import os

env = os.getenv('DJANGO_ENV')  # به طور پیش‌فرض، development را بارگذاری می‌کند

if str(env) == 'production':
    from .production import *
else:
    from .development import *
