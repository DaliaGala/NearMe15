import streamlit as st
import pandas as pd
import pydeck as pdk

# Assume session is created as in your environment
session = st.connection('snowflake').session()

st.title("📍 What services are nearby us?")

postcode_input = st.text_input("Enter a UK postcode (e.g., SW1A 1AA):")
normalized_postcode = postcode_input.strip().replace(" ", "").upper()

# Add service selection dropdown
service = st.selectbox("Which service do you want to see?", options=["Schools", "Sports Gyms", "GPs"])

if normalized_postcode:
    # Query postcode centroid
    postcode_query = f"""
        SELECT PCD2, LAT, LON
        FROM RESIDENTIAL_POSTCODES.GEOLOCAL.GEOLOCAL_RESIDENTIAL_POSTCODE
        WHERE REPLACE(UPPER(PCD2), ' ', '') = '{normalized_postcode}'
        LIMIT 1
    """
    postcode_df = session.sql(postcode_query).to_pandas()

    if not postcode_df.empty:
        postcode_lat = postcode_df.iloc[0]["LAT"]
        postcode_lon = postcode_df.iloc[0]["LON"]

        st.success(f"Found postcode: {postcode_df.iloc[0]['PCD2']}")

        # Create postcode radius map data
        postcode_point = pd.DataFrame([{
            "latitude": postcode_lat,
            "longitude": postcode_lon,
            "label": "Postcode Area",
            "color": [0, 0, 200, 100]
        }])

        # Show postcode area map with a radius circle
        postcode_layer = pdk.Layer(
            "ScatterplotLayer",
            data=postcode_point,
            get_position='[longitude, latitude]',
            get_color='color',
            get_radius=500,  # radius in meters
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=postcode_lat,
            longitude=postcode_lon,
            zoom=12,
            pitch=0,
        )

        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[postcode_layer],
            tooltip={"text": "{label}"}
        ))

        # Depending on service selection, query the respective table
        if service == "Schools":
            query = f"""
                SELECT SCHOOLTYPE, SCHOOLNAME, WEBSITE, LATITUDE, LONGITUDE
                FROM A_TEAM.PUBLIC.SCHOOLS_ALL
                WHERE REPLACE(UPPER(POSTCODE), ' ', '') = '{normalized_postcode}'
            """
            df = session.sql(query).to_pandas()
            if not df.empty:
                st.success(f"Found {len(df)} school(s) in this postcode.")
                df_display = df.rename(columns={
                    "SCHOOLTYPE": "School Type",
                    "SCHOOLNAME": "School Name",
                    "WEBSITE": "School Website"
                })
                st.dataframe(df_display[["School Type", "School Name", "School Website"]], use_container_width=True)

            else:
                st.warning("No schools found for this postcode.")

        elif service == "Sports Gyms":
            query = f"""
                SELECT ADDR_POSTCODE, ADDR_HOUSENAME
                FROM A_TEAM.PUBLIC.SPORTS_CENTRES
                WHERE REPLACE(UPPER(ADDR_POSTCODE), ' ', '') = '{normalized_postcode}'
            """
            df = session.sql(query).to_pandas()
            if not df.empty:
                st.success(f"Found {len(df)} sports gym(s) in this postcode.")
                df_display = df.rename(columns={
                    "ADDR_HOUSENAME": "Sports Centre Name"
                })
                st.dataframe(df_display[["Sports Centre Name"]], use_container_width=True)

            else:
                st.warning("No sports gyms found for this postcode.")

        elif service == "GPs":
            query = f"""
                SELECT PRAC_CODE, POSTCODE, LOCAL_AUTHORITY
                FROM A_TEAM.PUBLIC.GP_PRACTICES
                WHERE REPLACE(UPPER(POSTCODE), ' ', '') = '{normalized_postcode}'
            """
            df = session.sql(query).to_pandas()
            if not df.empty:
                st.success(f"Found {len(df)} GP(s) in this postcode.")
                df_display = df.rename(columns={
                    "PRAC_CODE": "GP Practice Code",
                    "LOCAL_AUTHORITY": "Local Authority"
                })
                st.dataframe(df_display[["GP Practice Code", "Local Authority"]], use_container_width=True)

            else:
                st.warning("No GPs found for this postcode.")

    else:
        st.error("Postcode not found in the database.")
else:
    st.info("Please enter a postcode above.")
