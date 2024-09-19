import streamlit as st
import plotly.express as px
import pandas as pd

# Load and clean the data
data = pd.read_csv('Tourism Lebanon 2023.csv')

# Data Cleaning
columns_to_keep = [
    'Total number of restaurants', 
    'Town', 
    'Total number of guest houses', 
    'Total number of hotels', 
    'Total number of cafes',
    'Existence of touristic attractions prone to be exploited and developed - exists',
    'Existence of initiatives and projects in the past five years to improve the tourism sector - exists',
    'Existence of touristic attractions that can be expolited and developed - does not exist',
    'Tourism Index',
    'refArea'  
]
data_cleaned = data[columns_to_keep]
data_cleaned['Area'] = data_cleaned['refArea'].apply(lambda x: x.split('/')[-1])
data_cleaned = data_cleaned.drop(columns=['refArea'])

# Combine columns
data_cleaned['Existence of touristic attractions prone to be exploited and developed'] = (
    data_cleaned['Existence of touristic attractions prone to be exploited and developed - exists'].apply(lambda x: 1 if x == 1 else 0)
)
data_cleaned['Existence of touristic attractions prone to be exploited and developed'] = (
    data_cleaned['Existence of touristic attractions prone to be exploited and developed'] 
    & data_cleaned['Existence of touristic attractions that can be expolited and developed - does not exist'].apply(lambda x: 1 if x != -1 else 0)
)
data_cleaned = data_cleaned.drop(columns=[
    'Existence of touristic attractions prone to be exploited and developed - exists',
    'Existence of touristic attractions that can be expolited and developed - does not exist'
])
data_cleaned = data_cleaned.rename(columns={
    'Existence of initiatives and projects in the past five years to improve the tourism sector - exists': 
    'Existence of initiatives and projects in the past five years to improve the tourism sector'
})
data_cleaned = data_cleaned.drop_duplicates()
data_cleaned = data_cleaned.dropna()

# Overview of the dataset and objectives
st.title("Tourism in Lebanon 2023: Analysis and Insights")
st.write("""
### Overview:
This dataset includes various metrics related to tourism in different towns in Lebanon. 
It contains data about the number of restaurants, hotels, cafes, guest houses, and the tourism index for each town. 
Additionally, it includes information about the existence of initiatives to improve tourism in recent years.

### Objective:
The goal of this analysis is to explore the relationships between the tourism index and various tourism facilities. 
We also aim to understand how initiatives to improve tourism affect the tourism index.
""")

# Visualization 1: Relationship between Tourism Index and Number of Facilities
st.write("### Visualization 1: Relationship between Tourism Index and Number of Tourism Facilities")
facility = st.selectbox("Select a tourism facility", 
                        ['Total number of restaurants', 'Total number of hotels', 'Total number of cafes'])
fig1 = px.scatter(data_cleaned, x=facility, y='Tourism Index', 
                  color='Area', 
                  title=f'Tourism Index vs {facility} by Area',
                  labels={facility: facility, 'Tourism Index': 'Tourism Index'})
fig1.update_layout(width=1200, height=700, margin=dict(l=10, r=10, t=50, b=100), 
                   xaxis_title=facility, yaxis_title='Tourism Index')
fig1.update_xaxes(tickangle=45)  # Rotate the x-axis labels

st.plotly_chart(fig1, use_container_width=True)  # Make it responsive to full width
st.write(f"""
**Insights:** 
- This visualization shows us that areas with higher number of different facilities tend to have higher tourism index as compared to other areas with lower number of tourism facilities. For example, Matn District has the highest number of restaurants (100) and scores tourism index of 9. Also, Bsharri District scores a tourism index of 10 and has the highest number of hotels (20). Regarding the number of cafes, Tripoli District has the highest number of cafes (100) with a tourism index of 10. This makes the number of tourism facilities in each area a direct indication of its tourism attractiveness. 
""")

# Visualization 2: Presence or Absence of Tourism Initiatives by Area
st.write("### Visualization 2: Areas with Absence or Presence of Tourism Initiatives")

# Interact: Select either 0 (absence) or 1 (existence) of initiatives
initiative_status = st.selectbox("Select initiative status (0: Absence, 1: Existence)", options=[0, 1])

# Filter data based on the selected initiative status
filtered_data = data_cleaned[data_cleaned['Existence of initiatives and projects in the past five years to improve the tourism sector'] == initiative_status]

# Count the number of occurrences of each area in the selected category
area_count = filtered_data['Area'].value_counts().reset_index()
area_count.columns = ['Area', 'Count']

# Create a horizontal bar chart showing the count of areas with absence or presence of initiatives
fig2 = px.bar(area_count, x='Count', y='Area',
              title=f'Areas with {"Absence" if initiative_status == 0 else "Presence"} of Tourism Initiatives',
              orientation='h', 
              labels={'Count': 'Number of towns', 'Area': 'Area'},
              color_discrete_sequence=['#ff7f0e' if initiative_status == 0 else '#1f77b4'])  # Set appropriate colors for status

# Adjust layout
fig2.update_layout(width=1200, height=800, margin=dict(l=10, r=10, t=50, b=50))

# Display the chart
st.plotly_chart(fig2, use_container_width=True)

st.write(f"""
**Insights:** 
- This visualization shows the areas that lack important initiatives in recent years that aim to improve the tourism sector and the other areas that indicate the presence of those initiatives in its different towns. We can notice that Akkar governance is the most area lacking such initiatives as compared to Byblos district scoring significant presence of tourism initiatives in its towns. Noting from the previous visualization that Byblos is scoring a tourism index of 10; this shows the importance of presence of tourism initiatives in improving the tourism sector in an area.
""")
