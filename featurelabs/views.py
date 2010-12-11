from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from featureflipper.models import Feature


def index(request):
    feature_list = [
        (feature, {
                'enabled': request.features_panel.enabled(feature.name),
                'source': request.features_panel.source(feature.name)
                })
        for feature in Feature.objects.all()
    ]
    return render_to_response('featurelabs/index.html', {
            'feature_list': feature_list,
            'features_panel': request.features_panel,
            },  context_instance=RequestContext(request))
