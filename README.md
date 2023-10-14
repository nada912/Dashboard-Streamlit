# 📦 Data Visualization Project - NADIRE Nada

A dashboard using streamlit application.

## Technical guidelines :

The streamlit application must respect the following technical requirements :
- All the code must be organized in functions, if you can write comments, it is always better. Think modulable code, blocks of data processing, workflow steps. This will help you organize your code in modular functions
- 4 internal streamlit plots : st.line, st.bar_chart, st.scatter_chart, st.map
- 4 different external plots (histograms, Bar, Scatter or Pie charts) integrated with your application from external librairies like matplotlib, seaborn, plotly or Altair
- 4 interactive elements (checkbox, slider ....)
- Cache usage : cache for data loading and pre-processing
- Optional : A decorator that logs in a file the time execution interval in seconds (30 seconds, 2 seconds, 0.01 seconds, ...) and the timestamp of the call ()
- Optional : try to organize your functions calls into a main function in order to have a clear workflow of your application

## My files : 

I have four initial csv files that I'll be exploring for this project : 
- caracteristiques-2022.csv
- lieux-2022.csv
- usagers-2022.csv
- vehicules-2022.csv

I will list below the files that I created during this project : 

### clean-db.py : 

Python file where I'll explore the dataset, do some cleaning and create the dataframe that I'll be using for my visualizations.
There will be also the questions that I'll be answering with my visualizations.

### accidents.csv : 

The dataset that I created and will be using for the visualizations.

## viz_project.csv : 
Python file where all my visualizations will be stored.

