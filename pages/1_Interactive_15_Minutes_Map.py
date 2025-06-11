import streamlit as st
import pandas as pd
import pydeck as pdk
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="NearMe15 Service Plotter", layout="wide")

# Get the current credentials
session = st.connection('snowflake').session()

st.title("📍 What services are nearby us?")

# Textbox for postcode input
postcode_input = st.text_input("Enter a UK postcode (e.g., SW1A 1AA):")

# Normalize input (remove spaces, upper case)
normalized_postcode = postcode_input.strip().replace(" ", "").upper()

# Query only if user entered something
if normalized_postcode:
    # Use SQL-style LIKE for safe fuzzy matching if needed
    query = f"""
        SELECT PCD2, LAT, LON
        FROM RESIDENTIAL_POSTCODES.GEOLOCAL.GEOLOCAL_RESIDENTIAL_POSTCODE
        WHERE REPLACE(UPPER(PCD2), ' ', '') = '{normalized_postcode}'
        LIMIT 1
    """
    result_df = session.sql(query).to_pandas()

    if not result_df.empty:
        st.success(f"Found postcode: {result_df.iloc[0]['PCD2']}")
        
        # Plot on map
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=result_df.iloc[0]["LAT"],
                longitude=result_df.iloc[0]["LON"],
                zoom=12,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=result_df,
                    get_position='[LON, LAT]',
                    get_color='[0, 100, 200, 160]',
                    get_radius=500,
                )
            ]
        ))
    else:
        st.error("Postcode not found in the database.")
else:
    st.info("Please enter a postcode above.")