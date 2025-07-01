import json
import pathlib
import random

import dash
from dash import html, dcc, Output, Input
import dash_leaflet as dl
import dash_leaflet.express as dlx

# Load GeoJSON data
here = pathlib.Path(__file__)
with open(here.parent / "filtered_output.geojson", "r") as f:
    county_geojson = json.load(f)

# Extract features and assign random colors
for feature in county_geojson["features"]:
    feature["properties"]["style"] = {
        "fillColor": random.choice(["#ffcccc", "#cce5ff", "#d5f5e3", "#f9e79f"]),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6
    }

# Create Dash app
app = dash.Dash(__name__)
server = app.server

# Create GeoJSON layer with click support
geojson = dl.GeoJSON(
    data=county_geojson,
    id="geojson",
    options=dict(style=lambda feature: feature["properties"]["style"]),
    zoomToBoundsOnClick=True,
    hoverStyle=dict(weight=3, color="black", fillOpacity=0.7),
)

# App layout
app.layout = html.Div([
    html.Div([
        html.H2("NJ County Map"),
        dl.Map(center=[40.206, -74.766], zoom=8, children=[
            dl.TileLayer(),
            geojson
        ], style={'width': '100%', 'height': '400px'}),
        html.H4("Selected County:"),
        html.Div(id="selected-county", style={
            'padding': '10px',
            'fontWeight': 'bold',
            'fontSize': '18px',
            'color': '#333',
            'backgroundColor': '#e0e6ff',
            'border': '2px solid #b3b8ff',
            'borderRadius': '10px',
            'textAlign': 'center',
            'marginBottom': '20px'
        }),
    ], style={
        'width': '25%',
        'padding': '20px',
        'backgroundColor': '#f8f8f8',
        'float': 'left',
        'boxSizing': 'border-box'
    }),

    html.Div([
        *[
            html.Div([
                html.H3(f"📊 Indicator {i}"),
                html.P(f"Content for Indicator {i}")
            ], style={
                'textAlign': 'center',
                'backgroundColor': '#e0e6ff',
                'border': '2px solid #b3b8ff',
                'borderRadius': '15px',
                'padding': '20px',
                'marginBottom': '20px'
            }) for i in range(1, 14)
        ]
    ], style={
        'width': '75%',
        'padding': '20px',
        'float': 'left',
        'boxSizing': 'border-box'
    })
])

@app.callback(
    Output("selected-county", "children"),
    Input("geojson", "click_feature")
)
def display_selected_county(feature):
    if feature is None:
        return "Click a county on the map"
    return feature["properties"].get("NAME", "Unknown")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
