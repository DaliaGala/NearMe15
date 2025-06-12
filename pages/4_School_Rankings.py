import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🏫How do my local schools rank?")

school_postcode_input = st.text_input("Enter a Scottish postcode (e.g., AB34 5JN):")
normalized_school_postcode = school_postcode_input.strip().replace(" ", "").upper()

if normalized_school_postcode:
    schools_df = pd.read_csv("data/school_rankings.csv")
    school_rank_df = schools_df[schools_df['normalized_postcode'] == normalized_school_postcode]
    highschools_df = school_rank_df[school_rank_df["SCHOOL_TYPE"].str.lower() == "highschool"]

    if not highschools_df.empty:
        st.success(f"Found {len(highschools_df)} highschool(s) in this postcode.")
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
