from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django import forms

from featureflipper.models import Feature
from featurelabs.models import EnabledFeature
from featurelabs.models import UserFeatures

FEATURE_CHOICES = (
    (True, 'Enable'),
    (False, 'Disable')
)

class FeatureForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput())
    user_enabled = forms.TypedChoiceField(coerce=lambda x: x == "True",
                                     choices=FEATURE_CHOICES,
                                     widget=forms.RadioSelect, label='')

    def save(self, user):
        feature = Feature.objects.get(name=self.cleaned_data['name'])
        EnabledFeature.objects.set_enabled(user, feature,
                                           self.cleaned_data['user_enabled'])

class BaseFeatureFormSet(BaseFormSet):
    def save(self, user):
        for form in self.forms:
            form.save(user)

FeatureFormSet = formset_factory(FeatureForm, formset=BaseFeatureFormSet, extra=0)

@login_required
def index(request):
    if request.method == 'POST':
        formset = FeatureFormSet(request.POST)
        if formset.is_valid():
            formset.save(request.user)
            return HttpResponseRedirect('/features/')

    features = Feature.objects.all()

    user_features = dict(UserFeatures.features(request))
    initial = [{'name': x.name, 'user_enabled':
                    user_features.get(x.name, False)} for x in features]
    formset = FeatureFormSet(initial=initial)

    feature_list = [(feature, {
                'enabled': request.features_panel.enabled(feature.name),
                'source': request.features_panel.source(feature.name),
                'form': formset.forms[i]
                }) for i, feature in enumerate(features)]

    return render_to_response('featurelabs/index.html', {
            'feature_list': feature_list,
            'features_panel': request.features_panel,
            'formset': formset
            },  context_instance=RequestContext(request))
