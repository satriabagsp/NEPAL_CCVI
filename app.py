import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
from shapely.geometry import box
import numpy as np
from PIL import Image
from Page import dashboard, variabel, simulasi, landcover, climate

# Fullscreen
im = Image.open("Image/global-warming.png")
st.set_page_config(
        page_title="NEPAL CCVI DASHBOARD",
        page_icon=im,
        layout="wide",
    )

# Remove Whitespace, hamburger, and "Made with streamlit"
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title = 'NEPAL CCVI',
        menu_icon = 'ui-radios',
        options = ['CCVI Dashboard', 'Climate Condition', 'Landcover', 'Dimension Data', 'Simulation'],
        icons = ['bar-chart-line-fill', 'snow2', 'tree-fill', 'aspect-ratio-fill', 'calculator-fill']
    )

## Main Page
# if selected == 'Beranda':
#     st.title('Beranda')

if selected == 'CCVI Dashboard':
    dashboard.app()

if selected == 'Climate Condition':
    climate.app()

if selected == 'Landcover':
    landcover.app()

if selected == 'Dimension Data':
    variabel.app()

if selected == 'Simulation':
    simulasi.app()