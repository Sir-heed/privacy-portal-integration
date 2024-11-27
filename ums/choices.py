from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedWith(models.TextChoices):
    """
    3rd party used for creation.
    """

    PRIVACY_PORTAL = 'PRIVACY PORTAL', _('PRIVACY PORTAL')
    CUSTOM = 'CUSTOM', _('CUSTOM')
