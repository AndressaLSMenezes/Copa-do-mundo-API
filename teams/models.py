from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=30)
    titles = models.PositiveIntegerField(default=0)
    top_score = models.CharField(max_length=50)
    fifa_code = models.CharField(max_length=3)
    first_cup = models.DateField(blank=True, null=True)

    def __repr__(id, name, fifa_code):
        return f"[{id}] {name} - {fifa_code}"
