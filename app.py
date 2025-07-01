import dash
from dash import html, Output, Input, dcc
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json

# Load your GeoJSON data
with open("filtered_output.geojson") as f:
    geojson_data = json.load(f)

# Create a GeoJSON layer
geojson_layer = dl.GeoJSON(
    data=geojson_data,
    id="geojson",
    options=dict(style=dict(weight=2, color="#666", fillOpacity=0.5)),
    hoverStyle=dict(weight=4, color="#000", fillOpacity=0.7),
)

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3("New Jersey Counties Map (Click to Select)"),
    dl.Map(
        children=[
            dl.TileLayer(),
            geojson_layer,
        ],
        style={'width': '1000px', 'height': '600px'},
        center=[40.0583, -74.4057],  # Centered over NJ
        zoom=8
    ),
    html.Div(id="click-output", style={"marginTop": "20px", "fontSize": "20px"})
])

# Callback to display county name
@app.callback(
    Output("click-output", "children"),
    Input("geojson", "click_feature")
)
def display_click(feature):
    if feature:
        return f"You clicked on: {feature['properties']['NAME']} County"
    return "Click on a county to see its name."

if __name__ == "__main__":
    app.run(debug=True)
