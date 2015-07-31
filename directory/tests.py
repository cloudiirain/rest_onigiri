from django.test import TestCase
from django.contrib.auth.models import User
from directory.models import Tag, Creator, Contributor, Series, SeriesAlias, SeriesRating, Volume, Chapter, Translation

def generic_init():
    '''
    Basic function to initialize commonly used models
    '''
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    tag = Tag.objects.create(name='Action')
    creator = Creator.objects.create(name='Yuuji, Yuuji')
    contributor = Contributor.objects.create(name='cloudii')
    series = Series.objects.create(name='Oreshura', synopsis='Masuzu does cool things.')
    alias = SeriesAlias.objects.create(name='Ore no kanojo', series=series)
    volume = Volume.objects.create(name='Volume 1', series=series, order=1)
    chapter = Chapter.objects.create(name='Chapter 1', volume=volume, order=1)
    translation = Translation.objects.create(chapter=chapter, translator=contributor)

    creator.moderated_object.approve(moderated_by=user, reason='test')
    contributor.moderated_object.approve(moderated_by=user, reason='test')
    series.moderated_object.approve(moderated_by=user, reason='test')
    alias.moderated_object.approve(moderated_by=user, reason='test')
    volume.moderated_object.approve(moderated_by=user, reason='test')
    chapter.moderated_object.approve(moderated_by=user, reason='test')
    translation.moderated_object.approve(moderated_by=user, reason='test')

class ModerationTestCase(TestCase):
    '''
    Test django-moderation functionality
    '''
    def setUp(self):
        Series.objects.create(name="Oreshura", synopsis="Masuzu does cool things.")
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_unmoderated_object(self):
        series = Series.unmoderated_objects.get(name="Oreshura")
        self.assertEqual(series.moderated_object.moderation_status, 2)
        self.assertEqual(len(Series.objects.all()), 0)
        self.assertEqual(len(Series.unmoderated_objects.all()), 1)
        self.assertEqual(series.synopsis, "Masuzu does cool things.")
    
    def test_moderated_object(self):
        series = Series.unmoderated_objects.get(name="Oreshura")
        user = User.objects.get(username="john")
        series.moderated_object.approve(moderated_by=user, reason='Test approval')
        self.assertEqual(series.moderated_object.moderation_status, 1)
        approved = Series.objects.get(name="Oreshura")
        self.assertEqual(approved.synopsis, "Masuzu does cool things.")

class UnicodeTestCase(TestCase):
    '''
    Test the unicode method in most models
    '''
    def setUp(self):
        generic_init()

    def test_tag_unicode(self):
        self.assertEqual(Tag.objects.get(name='Action').__unicode__(), u'Action')

    def test_creator_unicode(self):
        self.assertEqual(Creator.objects.get(name='Yuuji, Yuuji').__unicode__(), u'Yuuji, Yuuji')

    def test_contributor_unicode(self):
        self.assertEqual(Contributor.objects.get(name='cloudii').__unicode__(), u'cloudii')

    def test_series_unicode(self):
        self.assertEqual(Series.objects.get(name='Oreshura').__unicode__(), u'Oreshura')

    def test_seriesalias_unicode(self):
        self.assertEqual(SeriesAlias.objects.get(name='Ore no kanojo').__unicode__(), u'Ore no kanojo')

    def test_volume_unicode(self):
        self.assertEqual(Volume.objects.get(pk=1).__unicode__(), u'Oreshura: Volume 1')

    def test_chapter_unicode(self):
        self.assertEqual(Chapter.objects.get(pk=1).__unicode__(), u'Oreshura: Volume 1 Chapter 1')

    def test_translation_unicode(self):
        self.assertEqual(Translation.objects.get(pk=1).__unicode__(), u'Oreshura: Volume 1 Chapter 1 (cloudii)')

class SeriesVolumeChapterTestCase(TestCase):
    def setUp(self):
        generic_init()

    def test_series_sortkey_save(self):
        oreshura = Series.objects.get(name="Oreshura")
        self.assertEqual(oreshura.sort_key, u'Oreshura')
        index = Series.objects.create(name="A Certain Magical Index", sort_key="Certain Magical Index")
        self.assertEqual(index.sort_key, u'Certain Magical Index')
        index.sort_key = ""
        index.save()
        self.assertEqual(index.sort_key, u'A Certain Magical Index')

class SerializersTestCase(TestCase):
    pass