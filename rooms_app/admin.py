from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "creator")
    search_fields = ("name",)