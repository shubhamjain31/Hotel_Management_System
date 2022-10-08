from django.contrib import admin
from django.apps import apps

myapp = apps.get_app_config('room')
for model in myapp.get_models():
    admin.site.register(model)