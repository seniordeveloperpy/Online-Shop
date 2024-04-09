
from django.apps import apps
from django.contrib import admin

all_models = apps.get_models()

models_list = []

for model in all_models:
    if not admin.site.is_registered(model):
        models_list.append(model)


for model_class in models_list:
    admin.site.register(model_class)
