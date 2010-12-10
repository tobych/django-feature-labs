from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms

from featureflipper.models import Feature


FEATURE_CHOICES = (
    (True, 'Enable'),
    (False, 'Disable')
)

# http://docs.djangoproject.com/en/dev/topics/forms/formsets/

# we now need a way of referencing the feature from the featureform
# - use a featurewidget that does this and renders stuff for the form?
# - or just store the feature.id?

class FeatureForm(forms.Form):
    enabled = forms.TypedChoiceField(coerce=bool, choices=FEATURE_CHOICES,
                                     widget=forms.RadioSelect)

from django.forms.formsets import BaseFormSet

class BaseFeatureFormSet(BaseFormSet):
    def save(self):
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            print form.cleaned_data['enabled']
               
from django.forms.formsets import formset_factory
FeatureFormSet = formset_factory(FeatureForm, formset=BaseFeatureFormSet, extra=0)


def index(request):

    if request.method == 'POST':
        formset = FeatureFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/features/')
    else:

        if request.user.is_authenticated():
            myfeatures = request.user.enabled_features.all().values_list('id', flat=True)

        feature_list = [
            (feature, {
                    'enabled': request.features_panel.enabled(feature.name),
                    'source': request.features_panel.source(feature.name),
                    'user': feature.id in myfeatures
                    })
            for feature in Feature.objects.all()
        ]

        formset = FeatureFormSet(initial=[{'enabled':True}, {'enabled':False}])

        return render_to_response('featurelabs/index.html', {
            'feature_list': feature_list,
            'features_panel': request.features_panel,
            'formset': formset
            },  context_instance=RequestContext(request))
