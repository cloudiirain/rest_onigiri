from moderation.moderator import GenericModerator

class SeriesModerator(GenericModerator):
    notify_user = False
    auto_approve_for_superusers = True
    auto_approve_for_staff = True