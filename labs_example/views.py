from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext

def index(request):
    return render_to_response('labs_example/index.html',
                              context_instance=RequestContext(request))
