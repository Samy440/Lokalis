# lokaliz/views.py
from django.shortcuts import render
from django.http import HttpResponse
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from opencage.geocoder import OpenCageGeocode
import folium
from geopy.geocoders import Nominatim
from decouple import config

# Create your views here.
def home(request):
    return render(request, 'home.html')

def result(request):
    return render(request, 'result.html')

def localize(request):
    if request.method == 'POST':
        num = request.POST.get("phone_number")
        le_num = phonenumbers.parse(num)
        la_location = geocoder.description_for_number(le_num, "fr")
        fournisseur = phonenumbers.parse(num)
        operateur = carrier.name_for_number(fournisseur, "fr")

        key = config("key")
        coordonnees = OpenCageGeocode(key)
        requete = str(la_location)
        reponse = coordonnees.geocode(requete)

        if reponse:
            lat = reponse[0]["geometry"]["lat"]
            lng = reponse[0]["geometry"]["lng"]

            my_map = folium.Map(location=[lat, lng], zoom_start=12)
            folium.Marker([lat, lng], popup=la_location).add_to(my_map)
            my_map.save("localis/templates/map.html")

            coordinates = f"{lat}, {lng}"
            geolocator = Nominatim(user_agent="Gelocaliz")
            user_location = geolocator.geocode(coordinates, addressdetails=True)

            return render(request, 'result.html', {'user_location': user_location, 'operateur': operateur})
        else:
            return HttpResponse("Adresse non trouvée pour le numéro de téléphone.")
    return render(request, 'home.html')


def map(request):
    return render(request, 'map.html')
