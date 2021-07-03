import jsonfield

from django.db import models

from players.models import Player, Position
from teams.models import Team
from enum import IntEnum


class EventTypes(IntEnum):
    CREATE_SYSTEM = 1
    CREATE_USER = 2

    UPDATE_SYSTEM = 3
    UPDATE_USER = 4

    DELETE_SYSTEM = 5
    DELETE_USER = 6

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class StatsEvent(models.Model):
    uid = models.UUIDField()
    index = models.IntegerField()

    event_type = models.IntegerField(
        choices=EventTypes.choices(), default=EventTypes.CREATE_SYSTEM)
    event = jsonfield.JSONField()

    class Meta:
        unique_together = ('uid', 'index',)


class StatsProjection(models.Model):
    uid = models.UUIDField(primary_key=True)
    index = models.IntegerField()

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    att_g = models.FloatField()
    att = models.IntegerField()
    yds = models.FloatField()
    avg = models.FloatField()
    yds_g = models.FloatField()
    td = models.IntegerField()
    lng = models.CharField(max_length=5)
    first_down = models.IntegerField()
    first_down_pct = models.FloatField()
    yard_20_p = models.IntegerField()
    yard_40_p = models.IntegerField()
    fum = models.IntegerField()

    # We will store longest touch down score
    lng_eq = models.IntegerField(default=0)

    class Meta:
        unique_together = ('uid', 'index',)

    def save(self, *args, **kwargs):
        touch_down_index = 150
        hasTouchDown = "T" in str(self.lng)

        if hasTouchDown:
            eq_worth = int(''.join(filter(str.isdigit, self.lng))
                           ) * touch_down_index
        else:
            eq_worth = int(self.lng)

        self.lng_eq = eq_worth
        # Call the "real" save() method.
        super(StatsProjection, self).save(*args, **kwargs)
