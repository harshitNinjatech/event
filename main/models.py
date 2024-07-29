from django.db import models


class SellModeChoice(models.TextChoices):
    ONLINE = 'online'
    OFFLINE = 'offline'


class StatusChoice(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Event(models.Model):
    event_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    sell_mode = models.CharField(max_length=55, choices=SellModeChoice.choices, default=SellModeChoice.ONLINE)
    status = models.CharField(max_length=55, choices=StatusChoice.choices, default=StatusChoice.ACTIVE)
    provider = models.CharField(max_length=50)
    json_data = models.TextField()
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ('-event_id',)
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.event_id}-{self.name}"
