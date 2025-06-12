import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("📍 What services are there within the 15 minutes radius?")
st.markdown("This page allows users to explore local public services available within their postcode area — such as schools, GP surgeries and sports facilities. By helping residents discover nearby services they may not have previously known about, the tool could support more informed decision-making and equitable access to essential resources which are close to their place of residence. It could be utilised both by individuals to promote awareness of the public infrastructure, but also by the public sector when planning said infrastructure and allocating resources.")

postcode_input = st.text_input("Enter a Scottish postcode (e.g., G74 2BP):")
normalized_postcode = postcode_input.strip().replace(" ", "").upper()
all_postcodes = pd.read_csv("data/postcodes.csv")

if normalized_postcode:
    postcode_df = all_postcodes[all_postcodes['normalized_postcode'] == normalized_postcode]

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
        with st.container():
            browse_services = st.radio("Do you want to browse services?", ["No", "Yes"])
            if browse_services == "Yes":
                st.markdown("Since this is a minimum viable product, not all postcodes have reliable associated data. If the postcode you inserted does not return any data, try AB21 9DG which has data for all three services.")
                service = st.selectbox("Which service do you want to see?", options=["Schools", "Sports Centres", "GPs"])
                if service == "Schools":
                    df = pd.read_csv("data/school_rankings.csv")
                    school_df = df[df['normalized_postcode'] == normalized_postcode]
                    if not school_df.empty:
                        st.success(f"Found {len(school_df)} school(s) in this postcode.")
                        df_display = school_df.rename(columns={
                            "SCHOOL_TYPE": "School Type",
                            "SCHOOLNAME": "School Name",
                            "WEBSITE": "School Website"
                        })
                        st.dataframe(df_display[["School Type", "School Name", "School Website"]], use_container_width=True)
                    else:
                        st.warning("No schools found for this postcode.")

                elif service == "Sports Centres":
                    df = pd.read_csv("data/sports_centres.csv")
                    gyms_df = df[df['normalized_postcode'] == normalized_postcode]
                    if not gyms_df.empty:
                        st.success(f"Found {len(gyms_df)} sports gym(s) in this postcode.")
                        df_display = gyms_df.rename(columns={
                            "NAME": "Sports Centre Name",
                            "SPORT": "Sports Available",
                            "PHONE": "Phone Number",
                            "EMAIL": "Email Address",
                            "OPENING_HOURS": "Opening Hours"
                        })
                        st.dataframe(df_display[["Sports Centre Name","Sports Available", "Phone Number", "Email Address", "Opening Hours"]], use_container_width=True)
                    else:
                        st.warning("No sports centres found for this postcode.")

                elif service == "GPs":
                    df = pd.read_csv("data/gp_practices.csv")
                    gps_df = df[df['normalized_postcode'] == normalized_postcode]
                    if not gps_df.empty:
                        st.success(f"Found {len(gps_df)} GP(s) in this postcode.")
                        df_display = gps_df.rename(columns={
                            "ADDRESS": "GP Name and Address",
                            "PRAC_CODE": "GP Practice Code"
                        })
                        st.dataframe(df_display[["GP Name and Address", "GP Practice Code"]], use_container_width=True)
                    else:
                        st.warning("No GPs found for this postcode.")
    else:
        st.error("Postcode not found in the database.")
else:
    st.info("Please enter a postcode above.")
