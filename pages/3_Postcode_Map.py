import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

st.title("Mapbox API call to present 15 minutes commutability!")

def update_map(postcode):
    postcode_df = pd.read_csv("data/postcodes.csv")
    result_df = postcode_df[postcode_df['PCD2'] == postcode]
    
    if not result_df.empty:
        coordinateslookup = str(result_df.iloc[0]['LON']) + ',' + str(result_df.iloc[0]['LAT'])
    else:
        st.error("Db lookup failed")
        return
    
    # Mapbox access token
    mapbox_token = "pk.eyJ1IjoiamFja2dpbG1vcmVuZXMiLCJhIjoiY21icnVzNHEzMGR0czJxczczcnZnMWRneiJ9.3cGk0vmW6fbFZ5bX82YUyQ"
    
    # Fetch GeoJSON data
    url = f"https://api.mapbox.com/isochrone/v1/mapbox/driving-traffic/{coordinateslookup}?contours_minutes=15&polygons=true&denoise=1&access_token=" + mapbox_token
    response = requests.get(url)
    geojson_data = response.json()
    
    # Extract coordinates
    coordinates = geojson_data['features'][0]['geometry']['coordinates'][0]
    lons, lats = zip(*coordinates)

    # Create map with polygon
    fig = go.Figure(go.Scattermapbox(
        fill = "toself",
        lon = lons,
        lat = lats,
        mode = "lines",
        fillcolor = "rgba(86, 144, 255, 0.3)",
        line=dict(color="blue", width=2)
    ))
    
    # Update layout with Mapbox configuration
    fig.update_layout(
        mapbox = {
            'accesstoken': mapbox_token,
            'style': "light",
            'center': {'lon': float(result_df.iloc[0]['LON']), 'lat': float(result_df.iloc[0]['LAT'])},
            'zoom': 10
        },
        margin = {'l':0, 'r':0, 'b':0, 't':0}
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Create a form
with st.form("postcode_form"):
    postcode = st.text_input("Enter a postcode:", "DD11 3FA")
    submitted = st.form_submit_button("Update Map")
    
    if submitted:
        update_map(postcode)
