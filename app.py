import dash
from dash import html, Output, Input
import dash_leaflet as dl
import json

# Load your GeoJSON data
with open("filtered_output.geojson") as f:
    geojson_data = json.load(f)

# Create a GeoJSON layer
geojson_layer = dl.GeoJSON(
    data=geojson_data,
    id="counties",
    options=dict(style=dict(weight=2, color="#666", fillOpacity=0.5)),
    hoverStyle=dict(weight=4, color="#000", fillOpacity=0.7),
)

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

# App layout
app.layout = html.Div([
    # Sidebar with map
    html.Div([
        html.H3("New Jersey Counties"),
        dl.Map(
            children=[dl.TileLayer(), geojson_layer],
            style={'width': '100%', 'height': '500px'},
            center=[40.0583, -74.4057],
            zoom=8
        )
    ], style={
        'width': '25%',
        'float': 'left',
        'padding': '20px',
        'backgroundColor': '#f8f8f8',
        'boxSizing': 'border-box'
    }),

    # Main content with selected county
    html.Div([
        html.H2("Selected School"),
        html.Div(id="county", style={
            'fontSize': '24px',
            'padding': '20px',
            'backgroundColor': '#e0e6ff',
            'border': '2px solid #b3b8ff',
            'borderRadius': '10px',
            'textAlign': 'center',
            'marginBottom': '20px',
            'minHeight': '100px'
        }),
    ], style={
        'width': '75%',
        'float': 'left',
        'padding': '20px',
        'boxSizing': 'border-box'
    }),
])

# Callback to display county name
@app.callback(
    Output("county", "children"),
    Input("counties", "clickData")
)
def capital_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['NAME']} County"
    else:
        return "Click on a county to see its name."

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
