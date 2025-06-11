import streamlit as st
import pandas as pd
import pydeck as pdk

# Assume session is created as in your environment
session = st.connection('snowflake').session()

st.title("🏫How do my local schools rank?")

postcode_input = st.text_input("Enter a UK postcode (e.g., SW1A 1AA):")
normalized_postcode = postcode_input.strip().replace(" ", "").upper()

if normalized_postcode:
    # Query postcode centroid
    school_query = f"""
            SELECT SCHOOL_TYPE, SCHOOLNAME, WEBSITE, LATITUDE, LONGITUDE, FY2016, FY2017, FY2018, FY2019, FY2020, FY2021, FY2022
            FROM A_TEAM.PUBLIC.ALL_SCHOOL_RANKINGS
            WHERE REPLACE(UPPER(POSTCODE), ' ', '') = '{normalized_postcode}'
        """
    schools_df = session.sql(school_query).to_pandas()

    if not schools_df.empty:
        st.success(f"Found {len(schools_df)} school(s) in this postcode.")
      
        highschools_df = schools_df[schools_df["SCHOOL_TYPE"].str.lower() == "highschool"]

        if not highschools_df.empty:
            # Select ranking columns plus school name
            ranking_cols = ["FY2016", "FY2017", "FY2018", "FY2019", "FY2020", "FY2021", "FY2022"]
            ranking_data = highschools_df[["SCHOOLNAME"] + ranking_cols]

            # Melt the data to long format for plotting
            ranking_long = ranking_data.melt(
                id_vars=["SCHOOLNAME"],
                value_vars=ranking_cols,
                var_name="Year",
                value_name="Ranking"
            )

            # Convert Year to just the year number (optional)
            ranking_long["Year"] = ranking_long["Year"].str.replace("FY", "").astype(int)

            st.write("### Highschool Rankings Over Years")
            # Use line chart (Altair for better grouping)
            import altair as alt

            line_chart = alt.Chart(ranking_long).mark_line(point=True).encode(
                x="Year:O",
                y="Ranking:Q",
                color="SCHOOLNAME:N",
                tooltip=["SCHOOLNAME", "Year", "Ranking"]
            ).interactive()

            st.altair_chart(line_chart, use_container_width=True)
        else:
            st.info("No Highschool type schools found for this postcode.")
