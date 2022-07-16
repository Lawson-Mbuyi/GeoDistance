from django.shortcuts import render, get_object_or_404
from .models import Geo_distance
from .forms import DistanceForm
from geopy.geocoders import Nominatim
from .utils import geo_locate, cordinate_centralise, get_zoom
from geopy.distance import geodesic
import folium


def distance_compute(request):
    geo_object = get_object_or_404(Geo_distance, id=1)
    form = DistanceForm(request.POST or None)
    geolocator = Nominatim(user_agent='Geo_app')

    ip = '72.14.207.99'
    country, city, lat, lon = geo_locate(ip)
    #print('pays', country)
    #print('ville', city)
    location_lat = lat
    location_lon = lon

    current_location = geolocator.geocode(city)
    pointA = (location_lat, location_lon)

    m = folium.Map(width = 800, height=500, location=cordinate_centralise(location_lat, location_lon), zoom_start=8)

   # folium.Marker([location_lat, location_lon], tooltip = 'Zoomer', popup = city['city'],
                  #icon = folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination = form.cleaned_data.get('destination')
        encoded_destination = geolocator.geocode(destination)
        dest_latitude = encoded_destination.latitude
        dest_longitude = encoded_destination.longitude

        pointB = (dest_latitude, dest_longitude)
        distance_away = round(geodesic(pointA, pointB).km, 2)

        m = folium.Map(width=800, height=500, location=cordinate_centralise(dest_latitude, dest_longitude),
                       zoom_start=get_zoom(distance_away))

        folium.Marker([location_lat, location_lon], tooltip='Zoomer', popup=city['city'],
                      icon=folium.Icon(color='purple')).add_to(m)

        folium.Marker([dest_latitude, dest_longitude], tooltip='Zoomer', popup=encoded_destination,
                      icon=folium.Icon(color='red', icon='cloud')).add_to(m)

        line = folium.PolyLine(locations=[pointA, pointB], color='blue', weight=2)
        m.add_child(line)

        instance.location = current_location
        instance.distance = distance_away
        instance.save()

    m = m._repr_html_()

    context = {
        'distance': geo_object,
        'form': form,
        'map': m
    }
    return render(request, 'Geo_app/main.html', context)

