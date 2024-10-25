from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base_models import BaseModel


class StatusChoice(models.TextChoices):
    PENDING = 'pending', _('Pending')
    CONFIRMED = 'confirmed', _('Confirmed')
    CANCELLED = 'cancelled', _('Cancelled')


class Booking(BaseModel):
    stadium = models.ForeignKey('stadiums.Stadium', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField(_("Date"))
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))
    status = models.CharField(choices=StatusChoice.choices, default=StatusChoice.PENDING, max_length=20)

    class Meta:
        db_table = 'bookings'
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        indexes=[
            models.Index(fields=['stadium', 'status']),
            models.Index(fields=['date', 'start_time', 'end_time']),
        ]


    def __str__(self):
        return self.stadium.name
