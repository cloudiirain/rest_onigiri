from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from moderation import moderation
from directory.moderator import *

CREATORS = ( ("Author", 1),
                        ("Illustrator", 2),
                        ("Publisher", 3),
                        )

class Tag(models.Model):
    '''
    Represents a category (e.g. Action, Romance, Shounen) descriptive of light novel series
    '''
    name = models.CharField(max_length=20, unique=True, default="")

    def __unicode__(self):
        return self.name

class Creator(models.Model):
    '''
    Represents an author, illustrator, editor, publisher, etc of a light novel
    For people, use Lastname, Firstname format. Comma is required.
    '''
    name = models.CharField(max_length=100, default="")
    role = models.CharField(choices=CREATORS, default='Author', max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'role')
        ordering = ['name']
moderation.register(Creator)

class Contributor(models.Model):
    '''
    Represents a fan translators, editor, proofreader of a light novel translation
    '''
    name = models.CharField(max_length=100, unique=True, default="")
    #role

    def __unicode__(self):
        return self.name

moderation.register(Contributor)

class Series(models.Model):
    '''
    Represents a cohesive collection of books or volumes.
    note: name is the default name out of all the aliases
    '''
    name = models.CharField(max_length=100, default="")
    sort_key = models.CharField(max_length=100, default="", blank=True)
    contributors = models.ManyToManyField(Creator)
    tags = models.ManyToManyField(Tag)
    hitcount = models.PositiveIntegerField(default=0)
    synopsis = models.TextField(blank=True, default="")
    image = models.URLField(null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''
        If no sort key is provided, use the series name as the sort key
        '''
        if self.sort_key == "":
            self.sort_key = self.name
        super(Series, self).save(*args, **kwargs)
moderation.register(Series, SeriesModerator)

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
moderation.register(SeriesAlias)

class SeriesRating(models.Model):
    '''
    Allows registered users to vote for each series once
    '''
    series = models.ForeignKey(Series, null=True)
    user = models.ForeignKey(User, null=True)
    score = models.PositiveIntegerField(null=True)

    # Need a model manager to aggregate and calculate scores

class Volume(models.Model):
    '''
    Represents a physical book, belonging to a series of light novels
    '''
    name = models.CharField(max_length=100, default="")
    series = models.ForeignKey(Series, null=True)
    order = models.IntegerField(null=True)
    image = models.URLField(null=True)

    def __unicode__(self):
        return str(self.series) + ": " + self.name

    class Meta:
        unique_together = ('series', 'order')
        ordering = ['series', 'order']
moderation.register(Volume)

class Chapter(models.Model):
    '''
    Represents a portion of a given physical book or volume
    '''
    name = models.CharField(max_length=200, default="")
    volume = models.ForeignKey(Volume, null=True)
    order = models.IntegerField(null=True)

    def __unicode__(self):
        return str(self.volume) + " " + self.name

    class Meta:
        unique_together = ('volume', 'order')
        ordering = ['volume', 'order']
moderation.register(Chapter)

class Translation(models.Model):
    '''
    Represents a fan translation of a chapter
    '''
    url = models.URLField(null=True)
    translator = models.ForeignKey(Contributor, null=True)
    chapter = models.ForeignKey(Chapter, null=True)

    def __unicode__(self):
        return str(self.chapter) + " (" + str(self.translator) + ")"

moderation.register(Translation)
