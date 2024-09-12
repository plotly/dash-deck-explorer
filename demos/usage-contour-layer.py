"""
Adapted from: https://pydeck.gl/gallery/contour_layer.html


Location of livestock raised in New Mexico in the United States in 2006,
via the United Nations and FAOSTAT, with the source data viewable here: 
http://www.fao.org/faostat/en/

Locations for poultry are viewable in blue and cattle are in orange.

Overlaid with the satellite imagery from Mapbox to highlight the how t
errain affects agriculture.
"""

import os
import dash_deck
from dash import Dash, html
import pydeck as pdk
import pandas as pd

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")


CATTLE_DATA = (
    "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/nm_cattle.csv"
)
POULTRY_DATA = (
    "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/nm_chickens.csv"
)


HEADER = ["lng", "lat", "weight"]
cattle_df = pd.read_csv(CATTLE_DATA, header=None)
poultry_df = pd.read_csv(POULTRY_DATA, header=None)

cattle_df.columns = HEADER
poultry_df.columns = HEADER


view = pdk.data_utils.compute_view(cattle_df[["lng", "lat"]])

p75, p90, p99 = cattle_df["weight"].quantile([0.75, 0.9, 0.99])

STROKE_WIDTH = 5

CONTOURS_0 = [
    {"threshold": p75, "color": [0, 238, 224], "strokeWidth": STROKE_WIDTH},
    {"threshold": p90, "color": [0, 180, 240], "strokeWidth": STROKE_WIDTH},
    {"threshold": p99, "color": [0, 0, 240], "strokeWidth": STROKE_WIDTH},
]

p75, p90, p99 = poultry_df["weight"].quantile([0.75, 0.9, 0.99])

CONTOURS_1 = [
    {
        "threshold": p75,
        "color": [245, 245, 0],
        "strokeWidth": STROKE_WIDTH,
        "zIndex": 1,
    },
    {
        "threshold": p99,
        "color": [247, 150, 0],
        "strokeWidth": STROKE_WIDTH,
        "zIndex": 10,
    },
]


# in meters
CELL_SIZE = 3000

cattle = pdk.Layer(
    "ContourLayer",
    data=cattle_df,
    get_position=["lng", "lat"],
    contours=CONTOURS_0,
    cell_size=CELL_SIZE,
    aggregation='"MEAN"',
    get_weight="weight",
    pickable=True,
)

poultry = pdk.Layer(
    "ContourLayer",
    data=poultry_df,
    get_position=["lng", "lat"],
    contours=CONTOURS_1,
    cell_size=CELL_SIZE,
    aggregation='"MEAN"',
    get_weight="weight",
    pickable=True,
)


r = pdk.Deck(
    layers=[cattle, poultry],
    initial_view_state=view,
    map_style=pdk.map_styles.SATELLITE,
    mapbox_key=mapbox_api_token,
)


app = Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(r.to_json(), id="deck-gl", mapboxKey=r.mapbox_key, tooltip=True)
)


if __name__ == "__main__":
    app.run_server(debug=True)
