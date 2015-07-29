from django.db import models
from moderation.db import ModeratedModel

class Series(ModeratedModel):
    """
    Series: Model representing a collection of volumes or books
    """
    title = models.CharField(max_length=100, default="")
    synopsis = models.TextField(blank=True, default="")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title',]
        
"""
class RecentActivity(models.Model):
    # Use this class to track who changed each item of content and when
    # On save, track all relevant information

class Volume(models.Model):
   
    title = models.CharField(max_length=100, default="")
    series = models.ForeignKey(Series, null=True)
    order = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.series) + ": " + self.title

    class Meta:
        unique_together = ('series', 'order')
        ordering = ['series', 'order']

class Chapter(models.Model):
    title = models.CharField(max_length=200, default="")
    volume = models.ForeignKey(Volume, null=True)
    translator = models.CharField(max_length=50, default="")
    url = models.URLField(null=True)
    order = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.volume) + " " + self.title

    class Meta:
        ordering = ['volume', 'order']
"""