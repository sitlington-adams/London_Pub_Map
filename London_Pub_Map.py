#CREATING A MAP
#pip install folium
import folium
import pandas
data = pandas.read_csv("Pubs.csv") #Downloaded this from the internet
#dir(folium)
#help(folium.map)
#tiles = "Stamen Terrain" "OpenStreetMap" "Mapbox Bright" "Mapbox Control Room"

def colour_icon(borough): #This is a simple function used later to determine the colour of an icon. This are the borough codes for Waltham Forest, Newham, Hackney and Redbridge
    if borough == "E09000031":
        return "pink"
    if borough == "E09000025":
        return "darkgreen"
    if borough == "E09000026":
        return "orange"
    if borough == "E09000012":
        return "lightblue"
    else:
        return "lightgray"


map = folium.Map(location=[51.508190, -0.127958], zoom_start=6, tiles="Stamen Toner") # Generates a map, centred on Leicester square with zoom level 6. 
map.save("London-Pubs.html") #Saves the map
fgs = folium.FeatureGroup(name="Stations") #Creates a feature group in which to group children and layers
for coordinates in [[51.523819, -0.164190],[51.518892, -0.081448],[51.516875, -0.176632],[51.50455372,-0.088037808],[51.49588954,-0.141485017],[51.52927728,-0.123168404]]:
    fgs.add_child(folium.Marker(location=coordinates, popup=("Station"), icon=folium.Icon(color='black'))) #Adds some stations to the map

fgp = folium.FeatureGroup(name="Pubs")

lat = list(data["latitude"]) # Heading name in the downloaded csv file
longitude = list(data["longitude"])
pub_name = list(data['name'])
borough_code = list(data['borough_code'])
html = """<h4>Pub name:</h4>
Pub name: %s """

for lt, ln, pn, bc in zip(lat, longitude, pub_name, borough_code):
    iframe = folium.IFrame(html=html % str(pn), width=200, height=100)
    fgp.add_child(folium.Marker(location=[lt,ln], popup=folium.Popup(iframe), icon=folium.Icon(color=colour_icon(bc))))

fgl = folium.FeatureGroup(name="Greater London Boundary")
fgl.add_child(folium.GeoJson(data=(open("greaterlondon.json", "r", encoding="utf-8-sig").read()))) #This adds a polygon layer consisting of the outskirts of greater london

map.add_child(fgs)
map.add_child(fgp)
map.add_child(fgl)
map.add_child(folium.LayerControl())
map.save("London-Pubs.html")
print("Map Saved")