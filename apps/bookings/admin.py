from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'stadium', 'date', 'start_time', 'end_time', 'status')
    list_filter = 'status',
    date_hierarchy = 'date'
    raw_id_fields = ('creator', 'updater', 'deleter', 'stadium',)
