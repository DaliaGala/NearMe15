import streamlit as st
import altair as alt
import pandas as pd

st.title("🙁How much crime is there locally?")

# Query to get crime counts by group description
result_df = pd.read_csv("data/crime.csv")
st.markdown("Hover over the pie chart to read the numbers associated with each crime.")

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
