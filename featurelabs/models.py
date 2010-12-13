from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from featureflipper.models import Feature
from featureflipper import FeatureProvider

class EnabledFeatureManager(models.Manager):
    def set_enabled(self, user, feature, enabled):
        try:
            object = self.get(user=user, feature=feature)
        except self.model.DoesNotExist:
            if enabled:
                self.create(feature=feature, user=user)
                print "created"
        else:
            if not enabled:
                object.delete()
                print "deleted"


class EnabledFeature(models.Model):

    feature = models.ForeignKey(Feature, related_name='users')
    user = models.ForeignKey(User, related_name='enabled_features')
    objects = EnabledFeatureManager()

    class Meta:
        verbose_name_plural = "enabled features"
        unique_together = (("feature", "user"),)

    def __unicode__(self):
        return self.feature.__unicode__()


from featureflipper import FeatureProvider
class UserFeatures(FeatureProvider):
    source = 'user'
    @staticmethod
    def features(request):
        if request.user.is_authenticated():
            user_features = request.user.enabled_features.all().values_list('feature__name', flat=True)
            return [(x, True) for x in user_features]
        else:
            return []
