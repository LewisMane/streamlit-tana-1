import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
from streamlit_folium import folium_static

st.set_page_config(page_title='Tana GIS')

st.write("""
# TANA WATER WORKS DEVELOPMENT AGENCY WEB GIS

This web app consists of a web map displaying projects under TWWDA
""")

map_1 = folium.Map(location=[-1.26, 37.888], zoom_start=6, control_scale=True)

####################################
##### load the geojson layers and assign them a variable
UHC_PROJECTS = gpd.read_file("./data/UHC_PROJECTS.geojson")
ADB_PROJECTS = gpd.read_file("./data/ADB_PROJECT.geojson")
CC_PROJECT = gpd.read_file("./data/CROSS_COUNTY_PROJECT.geojson")
KENYA = gpd.read_file("./data/Counties.geojson")

###################################
###### add the layers to the web map
cc = folium.GeoJson(CC_PROJECT, name='CC Project').add_to(map_1)
adb = folium.GeoJson(ADB_PROJECTS, name='ADB Projects').add_to(map_1)
uhc = folium.GeoJson(UHC_PROJECTS, name='UHC Projects').add_to(map_1)
folium.GeoJson(KENYA, name='Kenya Counties',
              popup=folium.features.GeoJsonPopup(fields=['COUNTY'])).add_to(map_1)
####################################

#### styling ADB PROJECTS
for _, r in ADB_PROJECTS.iterrows():
    lat = r['geometry'].y
    lon = r['geometry'].x
    folium.Marker(location=[lat, lon],
                  tooltip='Click for ADB',
                  popup='Id: {} <br> Name: {}'.format(r['Id'], r['Name']),
                  icon=folium.Icon(color='green', icon='glyphicon-plane', prefix='glyphicon')).add_to(adb)

################################
##### styling CC projects
for _, r in CC_PROJECT.iterrows():
    lat = r['geometry'].y
    lon = r['geometry'].x
    folium.Marker(location=[lat, lon],
                  tooltip='Click for CC',
                  popup='Id: {} <br> Name: {}'.format(r['Id'], r['Names']),
                  icon=folium.Icon(color='orange', icon='glyphicon-info-sign', prefix='glyphicon')).add_to(cc)

##################################
###### styling UHC projects
for _, r in UHC_PROJECTS.iterrows():
    lat = r['geometry'].y
    lon = r['geometry'].x
    folium.Marker(location=[lat, lon],
                  tooltip='Click for UHC',
                  popup='Id: {} <br> Name: {}'.format(r['Id'], r['Name']),
                  icon=folium.Icon(color='darkpurple', icon='glyphicon-tint', prefix='glyphicon')).add_to(uhc)

#############################
# adding the drawing tools
draw = plugins.Draw(export=True)

map_1.add_child(draw)

#########################
## adding the measure tools
measure_control = plugins.MeasureControl(position='topleft',
                                        active_color='red',
                                        completed_color='green',
                                        primary_area_unit='meters')


map_1.add_child(measure_control)
############################

# adding basemap layers
folium.raster_layers.TileLayer('Open Street Map').add_to(map_1)
folium.raster_layers.TileLayer('Stamen Terrain').add_to(map_1)
folium.raster_layers.TileLayer('Stamen Toner').add_to(map_1)
folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map_1)
folium.raster_layers.TileLayer('Cartodb Positron').add_to(map_1)
folium.raster_layers.TileLayer('Cartodb Dark_Matter').add_to(map_1)

####################################
folium.LayerControl(collapsed=True).add_to(map_1)

folium_static(map_1, width=700, height=500)
