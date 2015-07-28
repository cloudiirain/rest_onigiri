from django.db import models

class Series(models.Model):
    title = models.CharField(max_length=100, default="", verbose_name="Series Title")
    author = models.CharField(max_length=50, default="", verbose_name="Series Author")
    synopsis = models.TextField(blank=True, default="")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)