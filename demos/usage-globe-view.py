"""
Adapted from: https://pydeck.gl/gallery/globe_view.html

This demos the experimental Glove View from deck.gl/pydeck by using the GeoJSON 
and column layers. The data used contains global plant database and can be found here:
https://github.com/ajduberstein/geo_datasets

Custom ocean geoJSON polygons added by [danny-baker](https://github.com/danny-baker), adapted from [Natural Earth](https://www.naturalearthdata.com/downloads/50m-physical-vectors/) 
(Note there are still some artifact issues over the Americas).
Power stations have been coloured by their fuel type, with useful hovertip information added.

Notice that here, we are explicitly convert the r.to_json() into a python dictionary.
This is needed because the data contains NaN, which can't be parsed by the underlying
JavaScript JSON parser, but it can be parsed by Python's JSON engine.

"""
import os
import json
import dash
import dash_deck
import dash_html_components as html
import pydeck
import pandas as pd

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")


COUNTRIES = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_scale_rank.geojson"
POWER_PLANTS = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/global_power_plant_database.csv"
OCEANS = json.load(open('data/ne_50m_ocean.geojson', 'r', encoding='utf-8'))

df = pd.read_csv(POWER_PLANTS)

def color_by_fuel(fuel_type):
    if fuel_type.lower() in "nuclear": return [10, 230, 120] #green
    elif fuel_type.lower() in ("wave and tidal", "hydro"): return [13, 23, 130] #dark blue
    elif fuel_type.lower() in "wind": return [106, 21, 176] #windy purple           
    elif fuel_type.lower() in ("biomass", "waste"): return [10, 230, 120] #purple
    elif fuel_type.lower() in "solar": return [250, 242, 2] #yellow
    elif fuel_type.lower() in "geothermal": return [156, 94, 19] #brown
    elif fuel_type.lower() in ("coal", "oil", "petcoke"): return [43, 42, 43] #black
    else: return [60,60,60]         

df["color"] = df["primary_fuel"].apply(color_by_fuel)

view_state = pydeck.ViewState(latitude=51.47, longitude=0.45, zoom=1.30)   
view = pydeck.View(type="_GlobeView", controller=True, width='100%', height='100%')

layers = [
                
    pydeck.Layer(
        "GeoJsonLayer",
        id="base-map-ocean",
        data=OCEANS,
        stroked=False,
        filled=True, 
        pickable=False, #Key difference in this layer as we don't want tooltips when hovering over the ocean
        auto_highlight=True,
        get_line_color=[60, 60, 60],
        get_fill_color=[134, 181, 209],                
        opacity=0.5,                
    ),

    pydeck.Layer(
        "GeoJsonLayer",
        id="base-map",
        data=COUNTRIES,
        stroked=False,
        filled=True,
        get_line_color=[60, 60, 60],
        get_fill_color=[160, 160, 160],
        opacity=1,
    ),

    pydeck.Layer(
        "ColumnLayer",
        id="power-plant",
        data=df,
        get_elevation="capacity_mw",
        get_position=["longitude", "latitude"],
        elevation_scale=150,
        pickable=True,
        auto_highlight=True,
        radius=10000,
        get_fill_color="color",
    ),
]

r = pydeck.Deck(
    views=[view],
    initial_view_state=view_state,
    layers=layers,            
    parameters={"cull": True},
)

app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
            json.loads(r.to_json()),
            id="deck-gl",                
            tooltip={"text": "{name}, {primary_fuel} plant, {capacity_mw}MW, {country_long}"},
        )
)

if __name__ == "__main__":
    app.run_server(debug=True)