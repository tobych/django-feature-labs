from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from featureflipper.models import Feature

class EnabledFeature(models.Model):

    feature = models.ForeignKey(Feature, related_name='users')
    user = models.ForeignKey(User, related_name='enabled_features')

    class Meta:
        verbose_name_plural = "enabled features"

    def __unicode__(self):
        return self.feature.__unicode__()
