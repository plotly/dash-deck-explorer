"""
Adapted from: https://pydeck.gl/gallery/trips_layer.html

Plot of a single vehicle trip within San Francisco, fading in from the origin.

Adapted from a deck.gl documentation example.
"""
import os
import dash_deck
from dash import Dash, html
import pydeck as pdk
import pandas as pd

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")

TRIPS_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.trips.json"  # noqa

df = pd.read_json(TRIPS_LAYER_DATA)

df["coordinates"] = df["waypoints"].apply(lambda f: [item["coordinates"] for item in f])
df["timestamps"] = df["waypoints"].apply(
    lambda f: [item["timestamp"] - 1554772579000 for item in f]
)

df.drop(["waypoints"], axis=1, inplace=True)

layer = pdk.Layer(
    "TripsLayer",
    df,
    get_path="coordinates",
    get_timestamps="timestamps",
    get_color=[253, 128, 93],
    opacity=0.8,
    width_min_pixels=5,
    rounded=True,
    trail_length=600,
    current_time=500,
)

view_state = pdk.ViewState(
    latitude=37.7749295, longitude=-122.4194155, zoom=11, bearing=0, pitch=45
)

# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state)


app = Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(r.to_json(), id="deck-gl", mapboxKey=mapbox_api_token)
)


if __name__ == "__main__":
    app.run_server(debug=True)
