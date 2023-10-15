# Data Visualization Project - NADIRE Nada

import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import plotly.figure_factory as ff

# Data source : data.gouv.fr
# Data chosen : Bases de données annuelles des accidents corporels de la circulation routière en 2022

#--------------------------------------------------------Step 1 : Explore & Clean Data----------------------------------------------------------
# display title
st.title ("Exploring and Cleaning Data")
#--------------------------------------------------------usagers dataframe----------------------------------------------------------------------
# display subtitle
st.markdown("## Usagers Dataframe")
usagers = pd.read_csv("usagers-2022.csv", delimiter=';', low_memory=False)

# Check the dimensions of the DataFrame
st.write("Shape of 'usagers' DataFrame:", usagers.shape)

# Explore the data using head()
st.write("First 10 rows of 'usagers' DataFrame:")
st.write(usagers.head(10))

# Check data types of columns
st.write("Data types of 'usagers' DataFrame:", usagers.dtypes)

# Check for missing values
st.write("Missing values in 'usagers' DataFrame:", usagers.isnull().sum())

# Drop the unnecessary columns 
usagers = usagers.dropna(subset=["an_nais"])
st.write("Drop the missing values in column 'an_nais' :", usagers)

# Check summary statistics of numerical columns
st.write("Summary statistics of numerical columns in 'usagers' DataFrame:")
st.write(usagers.describe())


#-----------------------------------------------------------lieux dataframe---------------------------------------------------------------------
# display subtitle
st.markdown("## Lieux Dataframe")

lieux = pd.read_csv("lieux-2022.csv", delimiter=';', low_memory=False)

# Check the dimensions of the DataFrame
st.write("Shape of 'lieux' DataFrame:", lieux.shape)

# Explore the data using head()
st.write("First 10 rows of 'lieux' DataFrame:")
st.write(lieux.head(10))

# Check data types of columns
st.write("Data types of 'lieux' DataFrame:", lieux.dtypes)

# Check for missing values
st.write("Missing values in 'lieux' DataFrame:", lieux.isnull().sum())

# Drop the unnecessary columns 
lieux = lieux.drop(["voie", "v2", "lartpc"], axis=1)
st.write("Drop the columns 'voie', 'v2' and 'lartpc' :", lieux)

# Check summary statistics of numerical columns
st.write("Summary statistics of numerical columns in 'lieux' DataFrame:")
st.write(lieux.describe())


#---------------------------------------------------------caractéristiques dataframe------------------------------------------------------------
# display subtitle
st.markdown("## Caractéristiques Dataframe")

caracteristiques = pd.read_csv("caracteristiques-2022.csv", delimiter=';', low_memory=False)

# Check the dimensions of the DataFrame
st.write("Shape of 'caractéristiques' DataFrame:", caracteristiques.shape)

# Explore the data using head()
st.write("First 10 rows of 'caractéristiques' DataFrame:")
st.write(caracteristiques.head(10))

# Check data types of columns
st.write("Data types of 'caractéristiques' DataFrame:", caracteristiques.dtypes)

# Check for missing values
st.write("Missing values in 'caractéristiques' DataFrame:", caracteristiques.isnull().sum())

# Drop the unnecessary columns 
caracteristiques = caracteristiques.dropna(subset=["adr"])
st.write("Drop the missing values in column 'adr' :", caracteristiques)

# Check summary statistics of numerical columns
st.write("Summary statistics of numerical columns in 'caractéristiques' DataFrame:")
st.write(caracteristiques.describe())


#------------------------------------------------------------véhicules dataframe---------------------------------------------------------------
# display subtitle
st.markdown("## Véhicules Dataframe")

vehicules = pd.read_csv("vehicules-2022.csv", delimiter=';', low_memory=False)

# Check the dimensions of the DataFrame
st.write("Shape of 'véhicules' DataFrame:", vehicules.shape)

# Explore the data using head()
st.write("First 10 rows of 'véhicules' DataFrame:")
st.write(vehicules.head(10))

# Check data types of columns
st.write("Data types of 'véhicules' DataFrame:", vehicules.dtypes)

# Check for missing values
st.write("Missing values in 'véhicules' DataFrame:", vehicules.isnull().sum())

# Drop the unnecessary columns 
vehicules = vehicules.drop(["occutc"], axis=1)
st.write("Drop the column 'occutc' :", vehicules)

# Check summary statistics of numerical columns
st.write("Summary statistics of numerical columns in 'véhicules' DataFrame:")
st.write(vehicules.describe())


#------------------------------------------------------------------Merge Dataframes------------------------------------------------------------
# Merge the dataframes based on 'Num_Acc'
main_df = usagers.merge(lieux, on='Num_Acc', how='inner')
main_df = main_df.merge(caracteristiques, left_on='Num_Acc', right_on='Accident_Id', how='inner')
main_df = main_df.merge(vehicules, on='Num_Acc', how='inner')

# Select only the necessary columns from the merged dataframe
columns_to_keep = ['Num_Acc', 'mois', 'lum', 'com', 'agg', 'int', 'atm', 'catr', 'surf', 'catv', 'id_usager', 'catu', 'grav', 'sexe', 'an_nais', 'trajet']
main_df = main_df[columns_to_keep]


#------------------------------------------------------------------Download Df------------------------------------------------------------------
# Save the main_df as a CSV file
main_df.to_csv(r'C:\Users\HP\Downloads\DataViz_Project_NADIRE_Nada\DataViz-Project-master\accidents.csv', index=False)

st.write("The merged dataframe main_df is saved as a CSV file named accidents.csv")
# Create a download button
st.download_button(
    label="Download main_df as CSV",
    key="download_main_df",
    data=main_df.to_csv().encode('utf-8'),
    file_name='accidents.csv',
    mime='text/csv',
)


#-----------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------Step 2 : Data Visualization------------------------------------------------------
st.markdown("## Identifying the questions to be answered")

st.markdown("#### A/ Determine the most accident-prone types of roads :")
# use 'catr' 
st.write("1. Which types of roads have the highest accident rate ?")
# use 'int' 
st.write("2. Are there specific road charcteristics associated with a higher likelihood of accidents ?")


st.markdown("#### B/ Analyze road conditions and environmental factors :")
#use 'surf'
st.write("1. How do road conditions (e.g., wet, icy, dry) correlate with accident occurrence and severity? ")
# use 'atm' 
st.write("2. Are certain weather conditions linked to an increased number of accidents ?")


st.markdown("#### C/ Explore vehicle types and their impact on mortality :")
# use 'catv' 
st.write("Is there a correlation between the type of vehicle and the severity of accidents in terms of mortality? ")


st.markdown("#### D/ Investigate age and gender of accident victims :")
# use 'sexe' and 'an_nais' 
st.write("How does the age distribution of accident victims vary by gender? ")

st.markdown("#### E/ Geographic analysis :")
# use 'com' 
st.write("Are there regions or areas that consistently experience higher accident rates? ")


st.markdown("#### F/ Investigate Usages and trajectories :")
# use 'trajet' 
st.write("Do certain types of trips or trajectories have a higher likelihood of accidents? ")
