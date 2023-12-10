import pandas as pd
import streamlit as st
from PIL import Image
import altair as alt
from utils import get_filtered_counts, mapped_colors, races
import os

# Read in the data
df = pd.read_csv("master.csv")

# Initialize the session state variable
if 'show_visuals' not in st.session_state:
    st.session_state.show_visuals = False

# Function to handle the button click
def on_click():
    st.session_state.show_visuals = not st.session_state.show_visuals

# Main layout container
main_container = st.empty()

if not st.session_state.show_visuals:

    # Inside the main container, layout your main page content
    with main_container.container():
        st.title("School to Prison Pipeline in Massachusetts")
        st.write("Exploring the Impact and Solutions")
        # Inject custom CSS with a script tag
        st.markdown("""
            <style>
            .big-font {
                font-size:20px !important;
                color: #004d99;
            }
            .highlight {
                background-color: #ffffcc;
                border: 1px solid #ffcc00;
                padding: 5px;
            }
            .split-bg {
                background: linear-gradient(to right, black 50%, yellow 50%);
            }
            .image-border {
                border-right: 2px solid #000; /* Border between images */
            }
            </style>
                    
            <script>
            document.addEventListener('DOMContentLoaded', function(event) {
                document.body.style.backgroundColor = '#e6f2ff';
            });
            </script>
        """, unsafe_allow_html=True)

        # Display Images with Border
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists("2.png"):
                image1 = Image.open("2.png")
                st.image(image1, use_column_width=True)
            else:
                st.error("Image 2.png not found")

        with col2:
            if os.path.exists("3.png"):
                image2 = Image.open("3.png")
                st.image(image2, use_column_width=True)
            else:
                st.error("Image 3.png not found")

        st.markdown('</div>', unsafe_allow_html=True)  # End of custom background

        # Insights on the School-Prison Pipeline
        st.markdown('<div class="big-font">The School-Prison Pipeline Phenomenon</div>', unsafe_allow_html=True)
        st.write("""
            The School-Prison Pipeline refers to the disturbing national trend wherein children are funneled out of public schools and into the juvenile and criminal justice systems. Factors contributing to this include harsh school policies and practices, and an increased role of law enforcement in schools. These practices disproportionately affect disadvantaged students, particularly in minority communities, leading to significant social and educational ramifications.
        """)

        st.button("Click here for interactive visuals", on_click=on_click)

# Display content from Race.py when the button is clicked
if st.session_state.show_visuals:
    st.button("Click here to go back", on_click=on_click)
    st.header("Overview of disproportionality in discipline")
    st.write("""
This section presents a critical examination of the disciplinary rates across different racial groups, casting light on the nuances of disproportionality in school discipline. Our analysis delves into the average discipline rates within each district, identifying instances where certain groups face disciplinary actions at rates higher than the district average — a clear indicator of disproportionality.

We go further to dissect how these rates vary within each disadvantaged group. This includes students with disabilities, English learners, and those from low-income backgrounds. By doing so, we not only unveil the overarching trends of disciplinary measures but also spotlight the disparities that exist within these subgroups.

Our approach demystifies the complex dynamics of school discipline, presenting the data in an accessible format that speaks to both academic professionals and the general public. This analysis is instrumental in fostering an understanding of how disciplinary practices in schools may disproportionately affect certain racial groups. It serves as a stepping stone towards advocating for more equitable educational policies and practices, ensuring that discipline in schools is fair, unbiased, and conducive to the learning and growth of all students.
""")

    main_container.empty()
    districts = df['District Name'].unique()
    district = st.sidebar.selectbox('Select a district', districts)

    # Create a dropdown for selecting a school within the district
    selected_school = st.sidebar.selectbox('Select a School:', df[df['District Name'] == district]['School Name'].unique())

    # Filter the dataframe
    df = df[(df['District Name'] == district) & (df['School Name'] == selected_school)]

    df['year'] = df['year'].apply(lambda y: str(y-1) + '-' + str(y)[2:])

    # Create a list of years
    years = df['year'].unique()

    # get dynamic column for selectbox
    categories = ['All', 'Students w/ Disabilities', 'English Learners', 'Low Income']
    cat_values = ['all', 'With Disability', 'English Learner', 'Low Income']

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

            # Create a bar chart for all races across years
            chart = alt.Chart(disciplinary_rate).mark_bar().encode(
                x=alt.X('Race/Ethnicity:O', axis=None),
                y='Disciplinary Rate',
                color=alt.Color(
                    'Race/Ethnicity:N',
                    scale=alt.Scale(
                        range = mapped_colors,
                        domain = races
                    )
                ),
                column='year:N'
            )
            st.write(chart)

            st.header("Race breakdown for " + cat_val + " students in " + district + " district")
            st.write("""
Building on our exploration of disproportionality in school discipline, we now turn our attention to a detailed race breakdown among all students in the State Totals District. This analysis crucially highlights the representation of each racial group within the student body, juxtaposing it against the proportion of students from these groups who face disciplinary actions.

In our visual representation, red bars in the bar chart symbolize the percentage of students disciplined within each racial category. This vivid color choice is deliberate, underscoring the critical insights these figures reveal. The contrast between the overall racial composition in the student body and the corresponding disciplinary percentages offers a stark visualization of how disciplinary measures are distributed across different racial groups.

This analysis is not just a collection of numbers; it is a narrative about equity and representation in our education system. By clearly illustrating these disparities, we aim to foster a deeper understanding of the challenges faced by various racial groups in the educational landscape. It's an essential step towards advocating for policies that ensure a balanced and fair approach to discipline, aligning disciplinary practices with the principles of equity and inclusion.
""")

            race_disciplined_counts = df_filtered.groupby(['Race/Ethnicity', 'year']).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Disciplined')).reset_index(name='disciplined_counts')

            total_disciplined_counts = df_filtered.groupby(['year']).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Disciplined', mode='sum')).reset_index(name='total_disciplined_counts')

            # merge the two dataframes on year
            merged_df = pd.merge(race_disciplined_counts, total_disciplined_counts, on='year')
            merged_df['percentage disciplined'] = merged_df['disciplined_counts']/merged_df['total_disciplined_counts'] * 100

            race_counts = df_filtered.groupby(['Race/Ethnicity', 'year']).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Eligible')).reset_index(name='eligible_counts')
            total_counts = df_filtered.groupby(['year']).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Eligible', mode='sum')).reset_index(name='total_counts')

            # merge the two dataframes on year
            population_df = pd.merge(race_counts, total_counts, on='year')
            population_df['percentage total'] = population_df['eligible_counts']/population_df['total_counts'] * 100

            race_breakdown = pd.concat([merged_df, population_df.drop(columns=['Race/Ethnicity', 'year'])], axis=1)
            bar = alt.Chart(race_breakdown).mark_bar().encode(
                color=alt.Color(
                    'Race/Ethnicity:N',
                    scale=alt.Scale(
                        range = mapped_colors,
                        domain = races
                    )
                ),
                x='Race/Ethnicity',
                y='percentage total'
            ).properties(
                width=alt.Step(40)  # controls width of bar.
            )

            tick = alt.Chart(race_breakdown).mark_tick(
                color='red',
                thickness=4,
                size=40,  # controls width of tick.
            ).encode(
                x='Race/Ethnicity',
                y='percentage disciplined'
            )

            chart2 = alt.layer(bar, tick).facet(column='year:N')

            st.write(chart2)

            # if cat_val != 'all':
            #     st.write("Impact of discipline on " + cat_val + " students in " + district + " district")
            #     for year in df_filtered['year'].unique():
            #         st.header(year)
            #         df_year_filtered = df_filtered[df_filtered['year'] == year]
            #         df_year_non_filtered = df_non_filtered[df_non_filtered['year'] == year]
            #         # get percentage of category students disciplined
            #         group_key = ['Race/Ethnicity']
            #         category_disciplined_percentage = df_year_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Disciplined')) / df_year_non_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Disciplined', mode='sum')) * 100
            #         category_disciplined_percentage = category_disciplined_percentage.reset_index(name='percentage_cat')
            #         category_disciplined_percentage['sample'] = 'Disciplined'

            #         # get percentage of category students in population
            #         category_students_percentage = df_year_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Eligible')) / df_year_non_filtered.groupby(group_key).apply(lambda grp: get_filtered_counts(grp, categories_to_check, 'Total Eligible', mode='sum')) * 100
            #         category_students_percentage = category_students_percentage.reset_index(name='percentage_cat')
            #         category_students_percentage['sample'] = 'Population'

            #         # concatenate the two dataframes
            #         concat_df = pd.concat([category_disciplined_percentage, category_students_percentage], axis=0)

            #         bar = alt.Chart(concat_df).mark_bar().encode(
            #         color=alt.Color(
            #                 'Race/Ethnicity:N',
            #             scale=alt.Scale(
            #                 range = mapped_colors,
            #                 domain = races
            #            )
            #         ),
            #         x='Race/Ethnicity',
            #         y='percentage_cat',
            #         column='sample:N'
            #     ).properties(
            #         width=alt.Step(40)  # controls width of bar.
            #     )

            #         st.write(bar)



    
                 
                