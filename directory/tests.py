from django.test import TestCase
from django.contrib.auth.models import User
from directory.models import Series, Volume, Chapter, Translation
from directory.models import Creator, Contributor, Tag
from directory.models import SeriesAlias, SeriesRating

def genericSetUp():
    '''
    Initialize objects used in most tests
    '''
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    tag = Tag.objects.create(name='boo')
    creator = Creator.objects.create(name='Yuuji, Yuuji', role='Author')
    contributor = Contributor.objects.create(name='steve', role='Translator')
    series = Series.objects.create(name='Oreshura', synopsis='Masuzu does cool things.')
    alias = SeriesAlias.objects.create(name='Ore no kanojo', series=series)
    rating = SeriesRating.objects.create(series=series, user=user, score=10)
    volume = Volume.objects.create(name='Volume 1', series=series, order=1)
    chapter = Chapter.objects.create(name='Chapter 1', volume=volume, order=1)
    #translation
    
    creator.moderated_object.approve(moderated_by=user, reason="test")
    contributor.moderated_object.approve(moderated_by=user, reason="test")
    series.moderated_object.approve(moderated_by=user, reason="test")
    alias.moderated_object.approve(moderated_by=user, reason="test")
    volume.moderated_object.approve(moderated_by=user, reason="test")
    chapter.moderated_object.approve(moderated_by=user, reason="test")
    #translation

class ModerationTestCase(TestCase):
    '''
    Test to ensure moderation system is working properly
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
    Test the unicode method on the models
    '''
    def setUp(self):
        genericSetUp()
        
    def test_tag_unicode(self):
        self.assertEqual(Tag.objects.get(name='boo').__unicode__(), u'boo')
    
    def test_creator_unicde(self):
        self.assertEqual(Creator.objects.get(name='Yuuji, Yuuji').__unicode__(), u'Yuuji, Yuuji')
        
    def test_contributor_unicode(self):
        self.assertEqual(Contributor.objects.get(name='steve').__unicode__(), u'steve')
    
    def test_series_unicode(self):
        self.assertEqual(Series.objects.get(name='Oreshura').__unicode__(), u'Oreshura')
    
    def test_series_alias_unicode(self):
        self.assertEqual(SeriesAlias.objects.get(name='Ore no kanojo').__unicode__(), u'Ore no kanojo')
    
    def test_volume_unicode(self):
        self.assertEqual(Volume.objects.get(pk=1).__unicode__(), u'Oreshura: Volume 1')
    
    def test_chapter_unicode(self):
        self.assertEqual(Chapter.objects.get(pk=1).__unicode__(), u'Oreshura: Volume 1 Chapter 1')
    
    def test_translation_unicode(self):
        pass

class SeriesVolumeChapterTestCase(TestCase):
    def setUp(self):
        genericSetUp()
       
    def test_series_sortkey_save(self):
        oreshura = Series.objects.get(name="Oreshura")
        self.assertEqual(oreshura.sort_key, u'Oreshura')
        index = Series.objects.create(name="A Certain Magical Index", sort_key="Certain Magical Index")
        self.assertEqual(index.sort_key, u'Certain Magical Index')
        index.sort_key = ""
        index.save()
        self.assertEqual(index.sort_key, u'A Certain Magical Index')