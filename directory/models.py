from django.db import models
from moderation.db import ModeratedModel

class Series(ModeratedModel):
    '''
    Represents a cohesive collection of books or volumes.
    '''
    name = models.CharField(max_length=100, default="")
    synopsis = models.TextField(blank=True, default="")

    def __unicode__(self):
        return self.name

class Volume(ModeratedModel):
    '''
    Represents a physical book, belonging to a series of light novels
    '''
    name = models.CharField(max_length=100, default="")
    series = models.ForeignKey(Series, null=True)
    order = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.series) + ": " + self.name

    class Meta:
        unique_together = ('series', 'order')
        ordering = ['series', 'order']

class Chapter(ModeratedModel):
    '''
    Represents a translation of a portion of a given physical book or volume
    '''
    name = models.CharField(max_length=200, default="")
    volume = models.ForeignKey(Volume, null=True)
    translator = models.CharField(max_length=50, default="", blank=True)
    url = models.URLField(null=True)
    order = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.volume) + " " + self.name

    class Meta:
        ordering = ['volume', 'order']
        
"""
class RecentActivity(models.Model):
    # Use this class to track who changed each item of content and when
    # On save, track all relevant information


"""