"""
Adapted from: https://pydeck.gl/gallery/geopandas_integration.html

This demos shows how to use the geopandas library in pydeck and Dash Deck.
"""
import os
import dash_deck
from dash import Dash, html
import pydeck as pdk
import pandas as pd
import geopandas as gpd

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

centroids = gpd.GeoDataFrame()
centroids["geometry"] = world.geometry.centroid
centroids["name"] = world.name

layers = [
    pdk.Layer("GeoJsonLayer", data=world, get_fill_color=[0, 0, 0],),
    pdk.Layer(
        "TextLayer",
        data=centroids,
        get_position="geometry.coordinates",
        get_size=16,
        get_color=[255, 255, 255],
        get_text="name",
    ),
]

r = pdk.Deck(layers, map_provider=None)

app = Dash(__name__)

app.layout = html.Div(dash_deck.DeckGL(r.to_json(), id="deck-gl"))


if __name__ == "__main__":
    app.run_server(debug=True)
