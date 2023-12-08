import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from utils import mapped_colors
# Read in the data
df = pd.read_csv("master.csv")

districts = df['District Name'].unique()
district = st.sidebar.selectbox('Select a district', districts)

df['year'] = df['year'].apply(lambda y: str(y-1) + '-' + str(y)[2:])
# Select a year
years = df['year'].unique()
year = st.sidebar.selectbox('Select a year', years)

# Filter the DataFrame for selected district and year
df = df[(df['District Name'] == district) & (df['year'] == year)]

# Allow user to optionally select a school, which will overwrite other visuals
schools = ['None'] + list(df['School Name'].unique())
school = st.sidebar.selectbox('Select a school to view the Race wise disciplinary rates and choose None to view all schools', schools)

st.write("""
## In-Depth School-Wise Disciplinary Analysis

This page offers a comprehensive exploration of disciplinary actions within schools, delving into the intricate dynamics of each institution. Our focus extends beyond mere statistics, as we unravel the layers of race and ethnicity, uncovering how these crucial factors intertwine within the educational framework of each school. Explore to understand the subtleties and nuances of school discipline, where every number tells a story, and every statistic reveals a deeper truth about our educational environments.
""")

# If a school is selected, show visuals for that school only
if school != 'None':
    df_school = df[df['School Name'] == school]

    # Categories for analysis
    categories = ['All', 'Students w/ Disabilities', 'English Learners', 'Low Income']

    # Create tabs for each category
    tabs = st.tabs(categories)

    for tab, category in zip(tabs, categories):
        with tab:
            # Filter data based on the category
            if category == 'All':
                df_s_filtered = df_school[df_school[['Students w/ Disabilities', 'English Learners', 'Low Income']].isnull().all(axis=1)]
            else:
                df_s_filtered = df_school[df_school[category].notnull()]

            # Exclude rows where 'Race/Ethnicity' is null for school-specific data
            df_s_filtered = df_s_filtered[df_s_filtered['Race/Ethnicity'].notnull()]

            # Group by 'Race/Ethnicity' and aggregate data
            grouped_df = df_s_filtered.groupby('Race/Ethnicity').agg({'Total Disciplined': 'sum', 'Total Eligible': 'sum'}).reset_index()

            # Calculate Discipline Rate
            grouped_df['Discipline Rate'] = grouped_df['Total Disciplined'] / grouped_df['Total Eligible']

            # Create a bar chart with disciplinary rate for each race/ethnicity
            chart = alt.Chart(grouped_df).mark_bar().encode(
                x=alt.X('Discipline Rate', axis=alt.Axis(format='%')),
                y=alt.Y('Race/Ethnicity', sort='-x'),
                color=alt.Color('Race/Ethnicity', scale=alt.Scale(range=mapped_colors))  # Using mapped_colours for the color scale
            ).properties(
                width=800,
                height=400,
                title=f"Discipline Rate by Race/Ethnicity in {category} for {school}"
            )
            st.altair_chart(chart, use_container_width=True)

else:
    # Categories for analysis
    categories = ['All', 'Students w/ Disabilities', 'English Learners', 'Low Income']

    # Create tabs for each category
    tabs = st.tabs(categories)

    for tab, category in zip(tabs, categories):
        with tab:
            # Filter data based on the category
            if category == 'All':
                df_filtered = df[df[['Students w/ Disabilities', 'English Learners', 'Low Income']].isnull().all(axis=1)]
            else:
                df_filtered = df[df[category].notnull()]

            # Group by school name and aggregate data
            grouped_df = df_filtered.groupby('School Name').agg({'Total Disciplined': 'sum', 'Total Eligible': 'sum'}).reset_index()

            # Calculate Discipline Rate
            grouped_df['Discipline Rate'] = grouped_df['Total Disciplined'] / grouped_df['Total Eligible']

            # Create horizontal bar chart with disciplinary rate for each school sorted descending
            chart = alt.Chart(grouped_df).mark_bar().encode(
                x=alt.X('Discipline Rate', axis=alt.Axis(format='%')),
                y=alt.Y('School Name', sort='-x'), color = alt.value('firebrick')
            ).properties(
                width=800,
                height=600,
                title=f"Discipline Rate in {category}"
            )

            st.altair_chart(chart, use_container_width=True)
