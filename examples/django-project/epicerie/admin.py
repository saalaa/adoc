from django.contrib import admin

from .models import (
    Potato, Tomato, Eggplant
)


@admin.register(Potato)
class PotatoAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    fields = ('name', 'weight')


@admin.register(Tomato)
class TomatoAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    fields = ('name', 'weight')


@admin.register(Eggplant)
class EggplantAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    fields = ('name', 'weight')
