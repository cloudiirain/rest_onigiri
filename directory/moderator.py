from moderation.moderator import GenericModerator

class SeriesModerator(GenericModerator):
    notify_user = False
    auto_approve_for_superusers = False
    auto_approve_for_staff = False

class VolumeModerator(GenericModerator):
    pass