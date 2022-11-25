from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
import pickle
import osmnx as ox
import folium
import geopy
import geopandas
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import networkx as nx
graph = pickle.load(open('D:/graph.pickle','rb'))
# graph = pickle.load(open('D:/riverside_graph.pickle','rb'))


def test(source,destination):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(source)
    sx=location.latitude
    sy = location.longitude
    loca = locator.geocode(destination)
    ex = loca.latitude
    ey = loca.longitude
    # return [sx,sy,ex,ey]
    orig_node = ox.nearest_nodes(graph, sx,sy)
    dest_node = ox.nearest_nodes(graph, ex,ey)

    shortest_route = nx.shortest_path(graph,
                                  orig_node,
                                  dest_node,
                                  weight='time')
    return shortest_route

def alternate_test(graph,source, destination):
    graph = ox.speed.add_edge_speeds(graph)
    graph = ox.speed.add_edge_travel_times(graph)
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(source)
    sx=location.latitude
    sy = location.longitude
    loca = locator.geocode(destination)
    ex = loca.latitude
    ey = loca.longitude
    orig_node = ox.nearest_nodes(graph, sx,sy)
    dest_node = ox.nearest_nodes(graph, ex,ey)
    route = ox.shortest_path(graph, orig_node, dest_node, weight="travel_time")
    return route

def hello():
    return test('Belmont, United States','Midwood, United States')

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

    list = [request.POST.get("handle", None),request.POST.get("handle2", None)]
    input1 = list[0]
    input2 = list[1]
    flag = 0
    alphabet_list = []
    for i in range(97,123):
        alphabet_list.append(i)
    for i in range(65,91):
        alphabet_list.append(i)
    alphabet_list.append(32)
    alphabet_list.append(44)

    for i in input1:
        if ord(i) not in alphabet_list:
            flag = 1
            break
    for i in input2:
        if ord(i) not in alphabet_list:
            flag = 1
            break

    if (flag==0):

        # graph_path = "maps/test.osm"
        # G = ox.graph_from_xml(graph_path, retain_all=True)
        # orig = ox.distance.nearest_nodes(G, X=X1 , Y=Y1)
        # dest = ox.distance.nearest_nodes(G, X =X2 , Y=Y2)
        # route = nx.shortest_path(G, orig, dest)
        # url = "http://127.0.0.1:5000/xyz?handle="+("%20".join(input1.split(' ')))+"&"+"handle2="+("%20".join(input2.split(' ')))
        # save_places = {'source':input1, 'dest':input2}
        # with open('D:/saved_places.json', 'w') as f:
        #     json.dump(save_places, f)

        route = test(input1, input2)
        # route = hello()
        # route = alternate_test(graph, input1, input2)
        m2 = ox.plot_route_folium(graph, route, color = 'red', dashed_array = 5)
        filepath = "D:/route.html"
        m2.save(filepath)
        import shutil

        filepath = 'maps/route.html'
        shutil.move('D:/route.html', 'D:/Spatial-Project/mysite/maps/templates/maps/route.html')
        return render(request, filepath, {})
    else:
        return render(request, 'maps/index.html', {'list': list, 'flag':flag})
