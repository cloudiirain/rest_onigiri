from django.test import TestCase
from django.contrib.auth.models import User
from directory.models import Series

class ModerationTestCase(TestCase):
    def setUp(self):
        Series.objects.create(title="Oreshura", synopsis="Masuzu does cool things.")
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_unmoderated_object(self):
        series = Series.unmoderated_objects.get(title="Oreshura")
        self.assertEqual(series.moderated_object.moderation_status, 2)
        self.assertEqual(len(Series.objects.all()), 0)
        self.assertEqual(len(Series.unmoderated_objects.all()), 1)
        self.assertEqual(series.synopsis, "Masuzu does cool things.")
    
    def test_moderated_object(self):
        series = Series.unmoderated_objects.get(title="Oreshura")
        user = User.objects.get(username="john")
        series.moderated_object.approve(moderated_by=user, reason='Test approval')
        self.assertEqual(series.moderated_object.moderation_status, 1)
        approved = Series.objects.get(title="Oreshura")
        self.assertEqual(approved.synopsis, "Masuzu does cool things.")

class SeriesTestCase(TestCase):
    def setUp(self):
        Series.objects.create(title="Oreshura", synopsis="Masuzu does cool things.")
    
    """
    def test_unicode(self):
        oreshura = Series.objects.get(title="Oreshura")
        sao = Series.objects.get(title="Sword Art Online")
        self.assertEqual(oreshura.__unicode__(), u'Oreshura')
        self.assertEqual(sao.synopsis, u'Kirito sux.')
    """
    