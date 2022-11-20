from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse

from django.shortcuts import get_object_or_404, render

# index returns the default page for the maps app
def index(request):
    return render(request, 'maps/index.html', {})

# show function takes the input from the index page of the app and
# shows some other output given the input
def show(request):
    try:
        import osmnx as ox
        import networkx as nx
    except:
        raise Http404("Failed to import modules")
    list = [request.POST.get("handle", None),request.POST.get("handle2", None)]
    input1 = list[0]
    input2 = list[1]
    if (input1.isalpha() and input2.isalpha()):
        return render(request, 'maps/show.html', {'list': list})
    else:
        return render(request, 'maps/index.html', {'list': list, 'flag':1})
