import streamlit as st
import altair as alt
from snowflake.snowpark.context import get_active_session

session = st.connection('snowflake').session()

st.title("🙁How much crime is there locally?")

# Query to get crime counts by group description
query = """
    SELECT 
        GROUP_DESCRIPTION,
        SUM(TOTALCRIMESTAT) as TOTAL_CRIMES
    FROM A_TEAM.PUBLIC.CRIME_2024_GLASGOW
    GROUP BY GROUP_DESCRIPTION
    ORDER BY TOTAL_CRIMES DESC
"""

result_df = session.sql(query).to_pandas()

# Create pie chart using Altair
pie_chart = alt.Chart(result_df).mark_arc().encode(
    theta='TOTAL_CRIMES',
    color='GROUP_DESCRIPTION',
    tooltip=['GROUP_DESCRIPTION', 'TOTAL_CRIMES']
).properties(
    width=400,
    height=400,
    title='Distribution of Crimes by Category in Glasgow 2024'
)

st.altair_chart(pie_chart, use_container_width=True)
