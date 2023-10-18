# Data Visualization Project - NADIRE Nada

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import ssl
from dico import dico_mapping  # Import the dico_mapping from dico.py
import time
import sys
import datetime


# Data source : data.gouv.fr
# Data chosen : Bases de données annuelles des accidents corporels de la circulation routière en 2022


st.set_page_config(
    page_title="Accidents Exploration 2022",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Function to set Streamlit page configuration
def set_streamlit_page_config():
    ssl._create_default_https_context = ssl._create_unverified_context  
    st.title("Accidents Exploration 🚗🔍")


# Function to include custom CSS styles
def include_custom_styles():
    try:
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("The 'style.css' file could not be found. Please make sure it exists in the same directory as your Python script.")


# Function to load data
# Use the @st.cache decorator to cache the data loading and pre-processing
@st.cache_data
def load_data():
    accidents = pd.read_csv("accidents.csv", delimiter=',', low_memory=False)
    return accidents


# Function to map old/new values from a dictionary to each column of the dataset  
@st.cache_data
def replacement(df, dicoRemplacement):
    df_new = df.replace(dicoRemplacement)
    return df_new 


# Function to create the sidebar
def create_sidebar(): 
    st.sidebar.header('Dashboard parameters')
    st.sidebar.markdown('''
    Dashboard created to explore the accidents dataset in France in 2022.
    ''')


# Function to display personal info
def personal_info():
    # Links GitHub & LinkedIn
    st.sidebar.markdown("[🔗 GitHub](https://github.com/nada912)") 
    st.sidebar.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/nada-nadire/)") 
    st.sidebar.markdown('''
    ---
    Created with ❤️ by Nada NADIRE.

    ''')


# Function to display the Key numbers
def display_statistics(df):
    st.markdown("## Accident Statistics")

    col1, col3, col5 = st.columns(3)
    col2, col4, col6 = st.columns(3)
    # Column 1: Count of Accidents
    total_accidents = len(df)
    col1.metric("Total Accidents", total_accidents)

    # Column 2: Variance % of Accidents
    accident_counts = df['Num_Acc'].value_counts()
    variance = accident_counts.var()
    rounded_variance = round(variance, 2)
    col2.metric("Variance % of Accidents", rounded_variance)

    # Column 3: Count of Deaths
    sum_deaths = df['grav'].eq(2).sum()  # Gravité 2 corresponds to 'Tué'
    col3.metric("Total Deaths", sum_deaths)

    # Column 4: Variance % of Deaths
    variance_grav = df['grav'].var()
    rounded_variance_grav = round(variance_grav, 2)
    col4.metric("Variance % of Deaths", rounded_variance_grav)

    # Column 5: Average Age
    average_age = df['an_nais'].mean()
    col5.metric("Average Age", round(average_age, 2))

    # Column 6: Percentage of Deaths
    total_accidents = len(df)
    percentage_deaths = round((sum_deaths / total_accidents) * 100, 2)
    col6.metric("Percentage of Deaths", f"{percentage_deaths}%")


# Function that gives the user the ability to change the grouping variable(s)
def init_groupings(df):
    # Filter categorical columns to include only "catr" and "dep"
    categorical_columns = {"Category": "catr", "Department": "dep"}
    # Create a selectbox in the sidebar to suggest to the user the different attributes
    grouping = st.sidebar.selectbox("Group by: ", list(categorical_columns.keys()))
    # We can't groupby again with the same column as the chosen one, so we drop it from further list options.
    remaining_options = [" — "] + [key for key in categorical_columns.keys() if key != grouping]
    grouping2 = st.sidebar.selectbox("and by : ", remaining_options)
    # The final list of keys to groupby is stored in final_group_keys
    final_group_keys = [categorical_columns[grouping]]
    
    if grouping2 != " — ":
        final_group_keys.append(categorical_columns[grouping2])
    
    return final_group_keys


# Function that gives the user the ability to choose only some levels for each grouping variable
def init_SelectionsLabels(df, grouping_keys):
    for element in grouping_keys:
        if element == "catr":
            label = "Category"
        elif element == "dep":
            label = "Department"
        else:
            label = element
        
        # List all levels one can use from the corresponding grouping variable
        level_options = list(pd.value_counts(df[element]).index)
        # Multiselect user interaction.
        # Use a label with the appropriate name (Category or Department)
        globals()["SelectedLabelsFor" + element] = st.sidebar.multiselect(
            label=f'Choice of levels for {label}', options=level_options
        )


# Function filtered by condition of road
def plot_accidents_by_cond_road(data):
    custom_colors1 = ["#FF5733", "#33FF57"]
    custom_colors2 = [ "#7791EF", "#DD77EF"]
    custom_colors3 = ["#DAF7A6", "#FFC300"]
    st.sidebar.title("Filter Options")
    selected_catr = st.sidebar.selectbox("Select Category of Road", data['catr'].unique())
    apply_filter = st.sidebar.button("Apply Filter", key="catr")

    if apply_filter:
        filtered_data = data[data['catr'] == selected_catr]
    else:
        # Use the unfiltered data if the button is not clicked
        filtered_data = data

    # Create the 'age' column
    current_year = datetime.datetime.now().year
    filtered_data['an_nais'] = filtered_data['an_nais'].fillna(0).astype(int)
    filtered_data['age'] = current_year - filtered_data['an_nais']

    c1, c2 = st.columns((6, 5))
    with c1:
        # Monthly accidents over the year
        months_order = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        data['mois'] = filtered_data['mois'].astype(str)
        monthly_data = filtered_data['Num_Acc'].groupby(filtered_data['mois']).count()
        monthly_data = monthly_data.reindex(months_order)

        fig = px.line(x=months_order, 
            y=monthly_data, 
            markers=True, 
            labels={'x': 'Month', 'y': 'Number of Accidents'}, 
            title='Monthly Accidents',
            color_discrete_sequence=custom_colors3)
        st.plotly_chart(fig)

    with c2:
        # Accidents inside / outside agglomeration
        agg_data = filtered_data['agg'].value_counts().reset_index()
        agg_data.columns = ['Agglomeration', 'Count']

        # Create a donut chart using Plotly Express
        fig = px.pie(agg_data, 
            names='Agglomeration', 
            values='Count',
            color_discrete_sequence=custom_colors2, 
            hole=0.4, 
            title='Accidents Inside/Outside Agglomeration')
        st.plotly_chart(fig)

    c3, c4 = st.columns((4, 3))
    with c3:
        # Accidents by category of vehicle
        vehicle_type_counts = filtered_data['catv'].value_counts()
        total_accidents = len(filtered_data)
        vehicle_type_percentages = (vehicle_type_counts / total_accidents) * 100

        vehicle_type_data = pd.DataFrame({
            "Vehicle Type": vehicle_type_percentages.index,
            "Percentage": vehicle_type_percentages.values
        })

        fig = px.bar(
            vehicle_type_data,
            x="Percentage",
            y="Vehicle Type",
            color_discrete_sequence=custom_colors1,
            title=f"Accidents by Vehicle Type (%) - Category of Road: {selected_catr}",
            labels={"Vehicle Type": "Type de véhicule", "Percentage": "Percentage of accidents (%)"}
        )
        st.plotly_chart(fig)

    with c4:
        # Calculate the age of individuals involved in accidents

        # Filter out rows with "sexe" equal to -1
        data_filtered = filtered_data[filtered_data['sexe'] != -1]

        # Group the filtered data by 'sexe' and 'age' and count the number of accidents
        grouped_data = data_filtered.groupby(['sexe', 'age']).size().reset_index(name='Count of accidents')

        # Create a Streamlit bar chart to visualize the data
        st.markdown("###### Count of Accidents by Gender and Age")
        st.bar_chart(grouped_data, x='sexe', y='Count of accidents')


# Function to display departments by accident range (st.bar_chart)
def display_departments_by_accident_range(df):
    st.markdown("## Departments by Accident Range")

    # Check if the 'total_accidents' column exists, and if not, create it
    if 'total_accidents' not in df.columns:
        df['total_accidents'] = df.groupby('dep')['Num_Acc'].transform('count')
    
    total_accidents = df['total_accidents'].max()  # Calculate the max value for the slider
    
    # Use two sliders to allow the user to choose an interval
    st.markdown("#### Select an interval of accidents")
    min_accidents = st.slider("Minimum number of accidents", min_value=0, max_value=total_accidents)
    max_accidents = st.slider("Maximum number of accidents", min_value=min_accidents, max_value=total_accidents)

    # Filter departments based on the chosen interval
    filtered_departments = df[(df['total_accidents'] >= min_accidents) & (df['total_accidents'] <= max_accidents)]

    if not filtered_departments.empty:
        # Display the corresponding departments
        st.write(f"Departments with a total of accidents between {min_accidents} and {max_accidents}:")
        # Create a bar chart to display the data
        chart_data = filtered_departments[['dep', 'total_accidents']]
        st.bar_chart(chart_data.set_index('dep'))


# Function to display accidents by gravity and usagers (st.bar_chart)
def plot_accidents_by_gravity_and_usager(data):
    data_filtered = data[data['grav'] != -1]
    grouped_data = data_filtered.groupby(['grav', 'catu']).size().reset_index(name='count')
    st.markdown("## Accidents by Gravity and Usager Type")

    # Create a selectbox to choose the type d'usager (catu)
    usager_types = data['catu'].unique()
    selected_usager = st.selectbox("Select Usager Type:", usager_types)

    # Filter the data based on the selected usager
    filtered_data = grouped_data[grouped_data['catu'] == selected_usager]

    # Create a Streamlit bar chart to visualize the data
    st.bar_chart(filtered_data, x='grav', y='count', use_container_width=True)


# Function filtered by luminosity
def plot_accidents_by_luminosity(data):
    custom_colors1 = ["#FF5733", "#33FF57"]
    custom_colors2 = [ "#7791EF", "#DD77EF"]
    custom_colors3 = ["#DAF7A6", "#FFC300"]

    filtered_data = data[(data['lum'] != -1)]
    selected_luminosity = st.sidebar.selectbox("Select Luminosity", filtered_data['lum'].unique())
    apply_filter = st.sidebar.button("Apply Filter", key="lum")

    if apply_filter:
        filtered_data = data[data['lum'] == selected_luminosity]
    else:
        # Use the unfiltered data if the button is not clicked
        filtered_data = data

    c1, c2 = st.columns((4, 3))
    with c1:
        # atmospheric conditions
        accidents_by_atm = filtered_data['Num_Acc'].groupby(filtered_data['atm']).count().reset_index()
        accidents_by_atm.columns = ['Conditions Atmosphériques', 'Number of Accidents']

        fig = px.histogram(
            accidents_by_atm,
            x='Conditions Atmosphériques',
            y='Number of Accidents',
            color_discrete_sequence=custom_colors2,
            labels={'Conditions Atmosphériques': 'Weather Conditions', 'Number of Accidents': 'Number of Accidents'},
            title='Number of Accidents by Weather Conditions'
        )

        st.plotly_chart(fig)
    
    with c2:
        # Route type
        data_filtered = filtered_data[(filtered_data['trajet'] != -1) & (filtered_data['trajet'] != 0)]
        accidents_by_trajet = filtered_data['Num_Acc'].groupby(data_filtered['trajet']).count().reset_index()
        accidents_by_trajet.columns = ['Route type', 'Number of Accidents']

        fig = px.histogram(
            accidents_by_trajet,
            x='Route type',
            y='Number of Accidents',
            color_discrete_sequence=custom_colors3,
            labels={'Route type': 'Route type', 'Number of Accidents': 'Number of Accidents'},
            title='Number of Accidents by Route type'
        )

        st.plotly_chart(fig)


# Function to measure execution time
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        st.text(f"Execution Time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper


# Decorator function to measure execution time and log to a file
def log_execution_time_to_file(log_filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get the current timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Measure the execution time
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            # Calculate the execution time in seconds
            execution_time = end_time - start_time

            # Log the execution time and timestamp to a file
            with open(log_filename, "a") as log_file:
                log_file.write(f"Timestamp: {timestamp}, Execution Time: {execution_time:.2f} seconds\n")

            return result

        return wrapper

    return decorator



# Main function to run the Streamlit app
# Usage of the decorator
@log_execution_time_to_file("execution_logs.txt")
def main():
    # set Streamlit page configuration
    set_streamlit_page_config()

    # include custom CSS styles
    include_custom_styles()

    # create sidebar
    create_sidebar()

    # load dataset
    accidents = load_data() 

    # display Key numbers
    display_statistics(accidents)

    # values mapping from an external dictionnary 
    accidents = replacement(accidents, dico_mapping)  

    # propose 1 or 2 grouping to be done
    #final_group_keys = init_groupings(accidents)

    # init the corresponding multiselect levels
    #init_SelectionsLabels(accidents, final_group_keys)

    # display external chart
    plot_accidents_by_cond_road(accidents)

    # display of the departments by accident range
    display_departments_by_accident_range(accidents)

    # display accidents by gravity and usagers    
    plot_accidents_by_gravity_and_usager(accidents)

    # display accidents by weather and luminosity
    plot_accidents_by_luminosity(accidents)
     
    # Create a checkbox to toggle personal info visibility
    show_personal_info = st.sidebar.checkbox("Show Personal Information")
    # Display personal info if the checkbox is checked
    if show_personal_info:
        personal_info()
    
    # measure execution time
    measure_execution_time(main)


if __name__ == '__main__':
    main()
