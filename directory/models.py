from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from moderation.db import ModeratedModel

SERIES_CONTRIBUTORS = [ ("Author", 1),
                        ("Illustrator", 2),
                        ("Publisher", 3),
                        ]

class Tag(models.Model):
    '''
    Represents a category (e.g. Action, Romance, Shounen) descriptive of light novel series
    '''
    name = models.CharField(max_length=20, unique=True, default="")

    def __unicode__(self):
        return self.name

class SeriesContributor(ModeratedModel):
    '''
    Represents an author, illustrator, editor, publisher, etc of a light novel
    For people, use Lastname, Firstname format. Comma is required.
    '''
    name = models.CharField(max_length=100, default="")
    role = models.CharField(choices=SERIES_CONTRIBUTORS, default='Author', max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'role')
        ordering = ['name']

class Series(ModeratedModel):
    '''
    Represents a cohesive collection of books or volumes.
    note: name is the default name out of all the aliases
    '''
    name = models.CharField(max_length=100, default="")
    sort_key = models.CharField(max_length=100, default="", blank=True)
    contributors = models.ManyToManyField(SeriesContributor)
    tags = models.ManyToManyField(Tag)
    hitcount = models.PositiveIntegerField(default=0)
    synopsis = models.TextField(blank=True, default="")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''
        If no sort key is provided, use the series name as the sort key
        If no SeriesAlias exists for the saved title, add it to SeriesAlias
        '''
        if self.sort_key == "":
            self.sort_key = self.name
        if len(SeriesAlias.objects.filter(name=self.name)) == 0:
            SeriesAlias.objects.create(name=self.name, series=self.pk)
        super(Series, self).save(*args, **kwargs)

class SeriesAlias(models.Model):
    '''
    Represents aliases for a Series name (e.g. OreShura)
    '''
    name = models.CharField(max_length=100, default="")
    slug = models.SlugField(max_length=100, unique=True, default="")
    series = models.ForeignKey(Series, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''
        Slugify the alias on every save.
        '''
        self.slug = slugify(self.name)
        super(SeriesAlias, self).save(*args, **kwargs)

class SeriesRating(models.Model):
    '''
    Allows registered users to vote for each series once
    '''
    series = models.ForeignKey(Series, null=True)
    user = models.ForeignKey(User, null=True)
    score = models.PositiveIntegerField(null=True)

    # Need a model manager to aggregate and calculate scores

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