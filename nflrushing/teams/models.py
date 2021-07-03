from django.db import models


class Team(models.Model):
    uid = models.UUIDField(primary_key=True)
    team_symbol = models.CharField(max_length=10, db_index=True)

    def __str__(self):
        return self.team_symbol
