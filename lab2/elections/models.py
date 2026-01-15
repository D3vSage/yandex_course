from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="counties")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["state", "name"], name="uniq_county_in_state")
        ]
        ordering = ["state__name", "name"]

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class CountyResult(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="results")
    current_votes = models.BigIntegerField()
    total_votes = models.BigIntegerField()
    percent = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["county__state__name", "county__name"]

    def __str__(self):
        return f"{self.county} total={self.total_votes}"
