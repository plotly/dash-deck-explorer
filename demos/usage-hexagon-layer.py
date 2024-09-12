"""
Adapted from: https://pydeck.gl/gallery/hexagon_layer.html

Personal injury road accidents in GB from 1979.

The layer aggregates data within the boundary of each hexagon cell.

This example is adapted from the deck.gl documentation.
"""
import os
import dash_deck
from dash import Dash, html
import pydeck as pdk
import pandas as pd

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")

HEXAGON_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv"  # noqa

# Define a layer to display on a map
layer = pdk.Layer(
    "HexagonLayer",
    HEXAGON_LAYER_DATA,
    get_position=["lng", "lat"],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1,
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36,
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state)

app = Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(r.to_json(), id="deck-gl", mapboxKey=mapbox_api_token)
)


if __name__ == "__main__":
    app.run_server(debug=True)
