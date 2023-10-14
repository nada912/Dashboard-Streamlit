# Data Visualization Project - NADIRE Nada

import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import plotly.figure_factory as ff

# Data source : data.gouv.fr
# Data chosen : Bases de données annuelles des accidents corporels de la circulation routière en 2022

accidents = pd.read_csv("accidents.csv", delimiter=';', low_memory=False)
