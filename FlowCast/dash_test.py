import dash
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc

# Sample Data for Zones
zone_data = [
    {
        "id": "biscayne",
        "name": "Biscayne Bay",
        "lat": 25.7751,
        "lon": -80.2105,
        "basin_name": "Florida Southeast Coast",
        "water_type": "Estuary",
        "size": "189.25 sq. miles",
        "nutrients": """
            Nutrients like nitrogen and phosphorus are naturally present in water 
            and necessary for healthy growth of plants and animals. However, 
            excessive nutrients can lead to harmful algal blooms.
        """,
        "chlorophyll": "Chlorophyll-a is an indicator of algal concentration in water bodies."
    },
    # Add more zones if needed
]

# Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    # Map
    dl.Map(
        [dl.TileLayer()] + [
            dl.Marker(
                id=zone["id"],
                position=(zone["lat"], zone["lon"]),
                children=dl.Tooltip(zone["name"])
            ) for zone in zone_data
        ],
        style={'width': '100%', 'height': '500px'},
        center=(25.7741, -80.1918),  # Centered near Florida
        zoom=8,
        id="map"
    ),

    # Hidden Modal for Zone Details
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
            dbc.ModalBody([
                html.Table([
                    html.Tr([html.Th("Waterbody Name:"), html.Td(id="modal-name")]),
                    html.Tr([html.Th("Basin Name:"), html.Td(id="modal-basin")]),
                    html.Tr([html.Th("Water Type:"), html.Td(id="modal-type")]),
                    html.Tr([html.Th("Size:"), html.Td(id="modal-size")]),
                ], style={"width": "100%"}),
                html.Br(),
                html.H5("Nutrients & Chlorophyll-a"),
                html.P(id="modal-nutrients"),
                html.P(id="modal-chlorophyll"),
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
            ),
        ],
        id="modal",
        is_open=False,
        size="lg"  # Large modal size to mimic the design
    )
])

# Callbacks
@app.callback(
    [Output("modal", "is_open"),
     Output("modal-title", "children"),
     Output("modal-name", "children"),
     Output("modal-basin", "children"),
     Output("modal-type", "children"),
     Output("modal-size", "children"),
     Output("modal-nutrients", "children"),
     Output("modal-chlorophyll", "children")],
    [Input(zone["id"], "n_clicks") for zone in zone_data] + [Input("close-modal", "n_clicks")]
)
def display_modal(*args):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]["prop_id"] == "close-modal.n_clicks":
        return [False, "", "", "", "", "", "", ""]

    # Find which marker was clicked
    clicked_zone = ctx.triggered[0]["prop_id"].split(".")[0]
    zone = next((z for z in zone_data if z["id"] == clicked_zone), None)

    if zone:
        return [
            True,  # Open the modal
            f"Details for {zone['name']}",
            zone["name"],
            zone["basin_name"],
            zone["water_type"],
            zone["size"],
            zone["nutrients"],
            zone["chlorophyll"]
        ]

    return [False, "", "", "", "", "", "", ""]

# Run App
if __name__ == "__main__":
    app.run_server(debug=True)
