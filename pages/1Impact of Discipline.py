import pandas as pd
import streamlit as st
import altair as alt
from utils import get_filtered_counts, mapped_colors, races

# Read in the data
df = pd.read_csv("master.csv")

districts = df['District Name'].unique()
district = st.sidebar.selectbox('Select a district', districts)

# Create a dropdown for selecting a school within the district
selected_school = st.sidebar.selectbox('Select a School:', df[df['District Name'] == district]['School Name'].unique())

# Filter the dataframe
df = df[(df['District Name'] == district) & (df['School Name'] == selected_school)]

df['year'] = df['year'].apply(lambda y: str(y-1) + '-' + str(y)[2:])

# Create a list of years
years = df['year'].unique()

st.write("""
### Comprehensive Analysis of the Impact of Disciplinary Actions on Disadvantaged Students

In this section, we embark on an in-depth investigation into the repercussions of disciplinary measures on students who are often marginalized in educational settings. This includes students with disabilities, English learners, and those from low-income backgrounds. By examining the differnces in impacts, we aim to foster a deeper understanding and awareness of the unique challenges faced by disadvantaged students. We encourage you to explore the subsequent tabs.
""")

# get dynamic column for selectbox
categories = ['Students w/ Disabilities', 'English Learners', 'Low Income']
cat_values = ['With Disability', 'English Learner', 'Low Income']

filter_cols = categories[1:]

# Create tabs for each category 
tabs = st.tabs(categories)

years_selected = st.sidebar.multiselect('Select years', years, default=years, key='year_select')
df_filtered_years = df[df['year'].isin(years_selected)]

for tab, cat, cat_val in zip(tabs, categories, cat_values):
        with tab:
            if cat_val == 'all':
                df_filtered = df_filtered_years
                categories_to_check = filter_cols
            else:
                categories_to_check = [col for col in filter_cols if col != cat]
                df_non_filtered = df_filtered_years.copy()
                df_non_filtered = df_non_filtered[df_non_filtered[cat].isnull()]
                df_filtered = df_filtered_years[df_filtered_years[cat] == cat_val]
            
            try:
                num = df_filtered.groupby(['Race/Ethnicity', 'year']).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Disciplined'))
                denom = df_filtered.groupby(['Race/Ethnicity', 'year']).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Eligible'))
                disciplinary_rate = num/denom * 100
                disciplinary_rate = disciplinary_rate.reset_index(name='Disciplinary Rate')
            except:
                import pdb; pdb.set_trace()

            if cat_val != 'all':
                st.write("Impact of discipline on " + cat_val + " students in " + district + " district")
                for year in df_filtered['year'].unique():
                    st.header(year)
                    df_year_filtered = df_filtered[df_filtered['year'] == year]
                    df_year_non_filtered = df_non_filtered[df_non_filtered['year'] == year]
                    # get percentage of category students disciplined
                    group_key = ['Race/Ethnicity']
                    category_disciplined_percentage = df_year_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Disciplined')) / df_year_non_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Disciplined', mode='sum')) * 100
                    category_disciplined_percentage = category_disciplined_percentage.reset_index(name='percentage_cat')
                    category_disciplined_percentage['sample'] = 'Disciplined'

                    # get percentage of category students in population
                    category_students_percentage = df_year_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Eligible')) / df_year_non_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Eligible', mode='sum')) * 100
                    category_students_percentage = category_students_percentage.reset_index(name='percentage_cat')
                    category_students_percentage['sample'] = 'Population'

                    # concatenate the two dataframes
                    concat_df = pd.concat([category_disciplined_percentage, category_students_percentage], axis=0)

                    bar = alt.Chart(concat_df).mark_bar().encode(
                    color=alt.Color(
                            'Race/Ethnicity:N',
                        scale=alt.Scale(
                            range = mapped_colors,
                            domain = races
                       )
                    ),
                    x='Race/Ethnicity',
                    y='percentage_cat',
                    column='sample:N'
                ).properties(
                    width=alt.Step(40)  # controls width of bar.
                )

                    st.write(bar)
