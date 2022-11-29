# from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
# from django.template import loader
from django.urls import reverse
import pickle
import osmnx as ox
import time
import folium
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import networkx as nx
graph = pickle.load(open('./maps/templates/maps/Brooklyn_Graph.pickle','rb'))
graph2 = pickle.load(open('./maps/templates/maps/Brooklyn_Graph.pickle','rb'))
hotspots = pickle.load(open('./maps/templates/maps/Hotspots.pickle','rb'))
hotspots2 = pickle.load(open('./maps/templates/maps/Hotspots2.pickle','rb'))

## Backend code starts here ##
def test(source,destination):
    for i in hotspots:
        if i==source or i==destination:
            continue
        graph2.remove_node(i)
    shortest_route = nx.shortest_path(graph2,
                                  source,
                                  destination,
                                  weight='time')
    return shortest_route
## Backend code ends here ##

from django.shortcuts import render

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
        ## Backend code starts here ##
        locator = Nominatim(user_agent="myGeocoder")
        location = locator.geocode(input1)
        sx=location.latitude
        sy = location.longitude
        loca = locator.geocode(input2)
        ex = loca.latitude
        ey = loca.longitude
        orig_node = ox.nearest_nodes(graph2, sy,sx)
        dest_node = ox.nearest_nodes(graph2, ey,ex)
        path = test(orig_node, dest_node)
        routes = []
        for i in hotspots:
            routes.append([i])
        routes.append(path)
        m2 = ox.folium.plot_route_folium(graph, path, tiles='openstreetmap')
        ox.folium.folium.Marker(location = [graph.nodes[orig_node]['y'],graph.nodes[orig_node]['x']], icon = folium.Icon(color='darkpurple') ).add_to(m2)
        ox.folium.folium.Marker(location = [graph.nodes[dest_node]['y'],graph.nodes[dest_node]['x']], icon = folium.Icon(color='darkpurple') ).add_to(m2)
        for i in hotspots:
            ox.folium.folium.Marker(location = [graph.nodes[i]['y'],graph.nodes[i]['x']], icon = folium.Icon(color='red') ).add_to(m2)
        for i in hotspots2:
            ox.folium.folium.Marker(location = [graph.nodes[i]['y'],graph.nodes[i]['x']], icon = folium.Icon(color='green') ).add_to(m2)
        filepath = "./route.html"
        m2.save(filepath)
        ## Backend code ends here ##

        # open both files
        with open(filepath,'r') as firstfile, open('./maps/templates/maps/route.html','w') as secondfile:
	        # read content from first file
            for line in firstfile:
		        # append content to second file
                secondfile.write(line)

        time.sleep(5)
        return render(request, 'maps/show.html', {'source':input1, 'dest':input2})
    else:
        return render(request, 'maps/index.html', {'list': list, 'flag':flag})

def route(request):
    return render(request, 'maps/route.html')
