from django.db import models

        
class Person(models.Model):
    """
    Model representing people contributing to a novel (e.g. author, illustrator, editor)
    """
    pass

class Tag(models.Model):
    """
    Model representing category tags that can be associated with series
    """
    pass

class SeriesTitle(models.Model):
    """
    Model representing the titles and aliases of any series
    """
    title = models.CharField(max_length=100, default="", verbose_name="Series Title")

class Series(models.Model):
    """
    Series: Model representing a collection of volumes or books
    """
    title = models.ManyToManyField(SeriesTitle, blank=True)
    contributors = models.ManyToManyField(Person, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    synopsis = models.TextField(blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title',]
        
        
class Volume(models.Model):
    """
    Volume: Model representing physical published light novels
    Every volume must belong to a series.
    """
    title = models.CharField(max_length=100, default="")
    series = models.ForeignKey(Series, null=True)
    order = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.series) + ": " + self.title

    class Meta:
        unique_together = ('series', 'number')
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
        ordering = ['volume', 'number']
        


class Contributor(models.Model):
    pass