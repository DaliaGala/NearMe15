import streamlit as st 
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="NearMe15: Reachability Impact Animation", layout="wide")

st.header("❄️Snowflake and Catalyst BI Public Sector Hackathon: Edinburgh, 11.06.2025")

st.write("This Streamlit app is the result of the work of Team 1, or A_TEAM during the Snowflake and Catalyst Public Service Hackathon in Edinburgh on 11.06.2025. Its aim was to learn more about what Snowflake can offer, promote collaboration across civil service departments and come up with projects which serve the public good, like social, environmental and health related causes. Team 1 members were Dalia Gala, Jack Gilmore, Ihsan Kerr, Lindsay Purves.")

st.image("images/hack_edinburgh_11062025.jpg", caption="Group photo of the hackathon attendees.", use_container_width=True)

st.markdown("📉 Public Transport Reachability Decline Across UK Cities")

st.write(
    """
    Recent research from the University of Bristol shows significant reductions in public transport reachability in many UK cities. This animated **bar chart** visualizes the decline in reachable destinations by city, showing the drop from 100% (pre-reduction) to current reported values.  
    Cities **Glasgow** and **Edinburgh** are highlighted in red to showcase comparatively moderate declines.  
    
    We can this visualization to understand how public transport accessibility has changed and why tools like NearMe15 are needed.
    Motivated by this observation, for our hackathon project, we wanted to create a prototype of an app which helps users assess how "15-minute" their city is—i.e., how many essential services are reachable within a short distance of a given postcode. NearMe15 is an early-stage MVP showing how local public data can be integrated into a single, user-friendly view. If developed further and deployed, it could aim to improve public awareness of neighbourhood accessibility and public service reachability as well as enable local authorities to focus their resources and improvement efforts where those are needed most..
    """
)

# Final values after decline (percentage of reachable destinations remaining)
data = {
    "CITY": [
        "SLOUGH & HEATHROW", "LONDON", "GLASGOW", "SOUTHEND", "LUTON", "EDINBURGH", "CRAWLEY", "NEWCASTLE",
        "GUILDFORD & ALDERSHOT", "LIVERPOOL", "WARRINGTON & WIGAN", "MEDWAY", "CAMBRIDGE", "MANCHESTER",
        "WOLVERHAMPTON & WALSALL", "BIRMINGHAM", "LEEDS", "BRISTOL", "SHEFFIELD", "NOTTINGHAM", "SOUTHAMPTON",
        "CARDIFF", "COVENTRY", "LEICESTER"
    ],
    "Target (%)": [
        82.4, 79.1, 78.1, 73.2, 71.5, 68.0, 64.1, 63.1, 59.6, 55.8, 55.0, 51.8,
        51.5, 51.5, 50.9, 47.9, 46.4, 40.1, 40.0, 38.4, 36.5, 33.7, 33.2, 33.0
    ]
}

df_final = pd.DataFrame(data)

# Highlight Glasgow and Edinburgh
df_final["Highlight"] = df_final["CITY"].apply(lambda x: "Highlighted" if x in ["GLASGOW", "EDINBURGH"] else "Other")

# Create animation frames - gradual decline from 100% to Target (%)
steps = 20
frames = []

for step in range(steps + 1):
    t = step / steps
    df_step = df_final.copy()
    df_step["Reachability (%)"] = 100 - (100 - df_step["Target (%)"]) * t
    df_step["Frame"] = step
    frames.append(df_step)

df_anim = pd.concat(frames)

# Animated bar chart
fig = px.bar(
    df_anim.sort_values("Reachability (%)", ascending=False),
    x="Reachability (%)",
    y="CITY",
    color="Highlight",
    orientation="h",
    animation_frame="Frame",
    range_x=[30, 105],
    labels={"Reachability (%)": "Reachability (%)", "CITY": "City"},
    color_discrete_map={
        "Highlighted": "#d62728",  # red for Glasgow & Edinburgh
        "Other": "#1f77b4"         # blue for others
    },
    title="Animated Decline in Night-Time Public Transport Reachability"
)

fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=800,
    margin=dict(l=100, r=40, t=60, b=40),
    showlegend=False,
    template="plotly_white"
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Source citation
st.markdown(
    """
    **Source:** University of Bristol, Centre for Urban Science and Data —  
    [Unveiling the Variability in Public Transport Services Across Great Britain](https://www.ubdc.ac.uk/news/unveiling-the-variability-in-public-transport-services-across-great-britain)
    """
)
