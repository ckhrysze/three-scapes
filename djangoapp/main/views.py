from django.shortcuts import render_to_response
from django_authopenid.forms import *
from django.contrib.auth.forms import *
from django.template import RequestContext, loader, Context

def index(request):
    form1 = OpenidSigninForm()
    form2 = AuthenticationForm()
    return render_to_response(
        "main_index.html",
        {
            'form1': form1,
            'form2': form2
            }, context_instance=RequestContext(request))
