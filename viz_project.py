# Data Visualization Project - NADIRE Nada

import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import plotly.figure_factory as ff
import plost
from streamlit.components.v1 import html
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
import ssl
import time


# Data source : data.gouv.fr
# Data chosen : Bases de données annuelles des accidents corporels de la circulation routière en 2022

st.set_page_config(page_title="Dashboard Storytelling", layout='wide', initial_sidebar_state='expanded')

# Function to set Streamlit page configuration
def set_streamlit_page_config():
    ssl._create_default_https_context = ssl._create_unverified_context  
    st.title("Data Visualization - Dashboard Storytelling")

# Function to include custom CSS styles
def include_custom_styles():
    try:
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("The 'style.css' file could not be found. Please make sure it exists in the same directory as your Python script.")
    
# Function to create the sidebar
def create_sidebar(): 
    st.sidebar.header('Dashboard parameters')

    st.sidebar.subheader('Heat map parameter')
    #time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

    st.sidebar.subheader('Donut chart parameter')
    #donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

    st.sidebar.subheader('Line chart parameters')
    #plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
    #plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

    st.sidebar.markdown('''
    ---
    Created with ❤️ by Nada NADIRE.
    ''')

# Function to load data
# Use the @st.cache decorator to cache the data loading and pre-processing
@st.cache_data
def load_data():
    df = pd.read_csv("accidents.csv", delimiter=',', low_memory=False)
    return df

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


# Function to display a donut chart & bar chart 
def display_external_chart(df):
    c1, c2 = st.columns((5, 5))
    with c1:
        st.markdown("## Bar Chart")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        month_counts = df['mois'].value_counts().reindex(range(1, 13))
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax1.bar(months, month_counts, color='blue', alpha=0.7)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Number of Accidents')
        ax1.set_title('Monthly Accident Counts')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig1)

    with c2:
        st.markdown("## Donut Chart")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        labels = ['Inside Agglomeration', 'Outside Agglomeration']
        sizes = [df['agg'].eq(1).sum(), df['agg'].eq(2).sum()]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.05, 0)
        ax2.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=explode)
        # draw circle
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig2 = plt.gcf()
        fig2.gca().add_artist(centre_circle)
        # Equal aspect ratio ensures that the pie chart is drawn as a circle
        ax2.axis('equal')
        st.pyplot(fig2)


# Function to measure execution time
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        st.text(f"Execution Time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

import time

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
    set_streamlit_page_config()
    include_custom_styles()
    create_sidebar()
    df = load_data()
    display_statistics(df)
    display_external_chart(df)
    measure_execution_time(main)


if __name__ == '__main__':
    main()
