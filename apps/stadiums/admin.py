from django.contrib import admin
from .models import Stadium, Image


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0
    fields = ('image', 'creator')


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    raw_id_fields = ('creator', 'updater', 'deleter')
    inlines = [ImageInline]