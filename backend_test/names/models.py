from django.db import models


class Names(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, default=None)
    url = models.CharField(max_length=255, null=True, blank=True, default=None)

    class Meta:
        db_table = "names"

    def __str__(self):
        return str(str(self.name) + ' ' + str(self.url))

