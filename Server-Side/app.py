import requests
from flask import Flask,request
import osmnx as ox
import folium
import geopy
import geopandas
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import networkx as nx
import pickle
import json
graph = pickle.load(open('../maps/templates/maps/graph.pickle','rb'))

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

app = Flask(__name__)
@app.route('/xyz')
def input_taken():
    f = open('D:/saved_places.json')
    saved_places = json.load(f)
    source = saved_places["source"]
    destination = saved_places["dest"]
    return test(source,destination)
@app.route('/akash')
def hello():
    return test('Belmont, United States','Midwood, United States')
if __name__ == '__main__':
    app.run()