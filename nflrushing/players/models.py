from django.db import models


class Player(models.Model):
    uid = models.UUIDField(primary_key=True)
    full_name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.full_name


class Position(models.Model):
    uid = models.UUIDField(primary_key=True)
    position_symbol = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.position_symbol
