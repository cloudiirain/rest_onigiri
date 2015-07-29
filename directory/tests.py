from django.test import TestCase
from django.contrib.auth.models import User
from directory.models import Series, Volume, Chapter

class ModerationTestCase(TestCase):
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

class SeriesVolumeChapterTestCase(TestCase):
    def setUp(self):
        series = Series.objects.create(name="Oreshura", synopsis="Masuzu does cool things.")
        volume = Volume.objects.create(name="Volume 1", series=series, order=1)
        chapter = Chapter.objects.create(name="Chapter 1", volume=volume, order=1)
        user = user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        
        series.moderated_object.approve(moderated_by=user, reason="test")
        volume.moderated_object.approve(moderated_by=user, reason="test")
        chapter.moderated_object.approve(moderated_by=user, reason="test")

    def test_series_unicode(self):
        oreshura = Series.objects.get(name="Oreshura")
        self.assertEqual(oreshura.__unicode__(), u'Oreshura')
        
    def test_volume_unicode(self):
        oreshura = Volume.objects.get(pk=1)
        self.assertEqual(oreshura.__unicode__(), u'Oreshura: Volume 1')
        
    def test_chapter_unicode(self):
        oreshura = Chapter.objects.get(pk=1)
        self.assertEqual(oreshura.__unicode__(), u'Oreshura: Volume 1 Chapter 1')