from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse

from django.shortcuts import get_object_or_404, render

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# index returns the default page for the maps app
def index(request):
    return render(request, 'maps/index.html', {})

# show function takes the input from the index page of the app and
# shows some other output given the input
def show(request):
    try:
        import osmnx as ox
        import networkx as nx
        from IPython.display import IFrame
    except:
        raise Http404("Failed to import modules")
    filepath = "maps/graph.html"
    # return render(request, filepath, {})

    list = [request.POST.get("handle", None),request.POST.get("handle2", None)]
    input1 = list[0]
    input2 = list[1]

    if (',' in input1 and ',' in input2):
        A = input1.split(',')
        X1,Y1 = A[0],A[1]
        B = input2.split(',')
        X2,Y2 = B[0],B[1]
    if (isfloat(X1) and isfloat(Y1) and isfloat(X2) and isfloat(Y2)):
        X1,Y1,X2,Y2 = float(X1),float(Y1),float(X2),float(Y2)
        # G = ox.graph_from_place("California, USA", network_type="drive")

        graph_path = "maps/test.osm"
        G = ox.graph_from_xml(graph_path, retain_all=True)
        # plot the street network with folium
        # m1 = ox.plot_graph_folium(G, popup_attribute="name", weight=2, color="#8b0000")
        # filepath = "D:\graph.html"
        # m1.save(filepath)
        orig = ox.distance.nearest_nodes(G, X=X1 , Y=Y1)
        dest = ox.distance.nearest_nodes(G, X =X2 , Y=Y2)
        route = nx.shortest_path(G, orig, dest)
        if type(route) == type(list):
            exit(1)
        m2 = ox.plot_route_folium(G, route, weight=10)
        filepath = "maps/route.html"
        m2.save(filepath)
        # import shutil

        # shutil.move('D:/route.html', 'maps/route.html')
        return render(request, filepath, {})
    else:
        return render(request, 'maps/index.html', {'list': list, 'flag':1})
