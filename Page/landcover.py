from turtle import width
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
from shapely.geometry import box
import numpy as np
from PIL import Image
import plotly.graph_objects as go

def app():
    st.title('Nepal Landcover')

    st.write('On this page you can see a distribution map of the land cover index of the selected provinces. \
            Please select the province, district, and land cover dimensions that you would like to see in the fields below. You can also see the comparability of the values of each variable in the forming dimensions \
            in the selected region.')


    indo = gpd.read_file('SHP NEPAL/Nepal LC Grid/LANDCOVER DISTRICT NEPAL GRID.shp')

    pil_c1, pil_c2, pil_c3 = st.columns(3)

    with pil_c1:
        pilihan_provinsi = st.selectbox(
            'Select Province.',
            ['ALL', '1', '2', 'BAGMATI', 'KARNALI', '5', 'SUDUR PASHCHIM', 'GANDAKI'],
            index=3)

        indo_prov = indo[indo.province == pilihan_provinsi]

        # Pilih Provinsi
        if pilihan_provinsi == 'ALL':
            indo_prov = indo
        else:
            indo_prov = indo[indo.province == pilihan_provinsi]
        
    with pil_c2:
        pilihan_kabkota = st.selectbox(
            'Select District.', ['ALL'] + indo_prov.district.drop_duplicates().to_list())

        # Pilih Kabkota
        if pilihan_kabkota == 'ALL':
            indo_prov = indo_prov
        elif pilihan_kabkota != 'ALL':
            indo_prov = indo_prov[indo_prov.district == pilihan_kabkota]

        # Get center
        bounds = indo_prov.total_bounds 
        polygon = box(*bounds)

        lat = polygon.centroid.y
        lon = polygon.centroid.x
        max_bound = max(abs(bounds[2] - bounds[0]), abs(bounds[3] - bounds[1])) * 111
        zoom = 12.7 - np.log(max_bound)

    with pil_c3:
        pilihan_dimensi = st.selectbox('Select Landcover Dimension.', ['NDVI'])
        if pilihan_dimensi == 'NDVI':
            var_dimensi = 'NDVI'
            var_color = 'Haline'
            var_range_color = [1,100]
        # elif pilihan_dimensi == 'ADAPTIVE':
        #     var_dimensi = 'adap_index'
        #     var_color = 'YlOrBr'
        #     var_range_color = [0,100]
        # elif pilihan_dimensi == 'EXPOSURE':
        #     var_dimensi = 'expo_index'
        #     var_color = 'PuBu'
        #     var_range_color = [0,100]
        # elif pilihan_dimensi == 'SENSITIVITY':
        #     var_dimensi = 'sensi_inde'
        #     var_color = 'dense'
        #     var_range_color = [0,100]
    
    st.write('---')


    fig2 = px.choropleth_mapbox(
        indo_prov,
        geojson=indo_prov.geometry, 
        locations=indo_prov.index,
        color = var_dimensi,
        color_continuous_scale=var_color,
        # range_color = var_range_color,
        mapbox_style="carto-positron",
        # mapbox_style="open-street-map",
        center={"lat": lat, "lon": lon},
        zoom=zoom,
        opacity=0.8,
        hover_name="district",
        height=500,
        hover_data={'NDVI':True},
        labels={'district':'District'}
    )
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig2.update_layout({'plot_bgcolor': '#2c2f38', 'paper_bgcolor': '#2c2f38'})

    if len(indo_prov) > 1 and len(indo_prov) < 70:
        st.subheader(f'{pilihan_provinsi} {pilihan_dimensi} DISTRIBUTION MAP')
    elif len(indo_prov) == 1:
        st.subheader(f'{pilihan_kabkota} - {pilihan_provinsi} {pilihan_dimensi} DISTRIBUTION MAP')
    else:
        st.subheader(f'NEPAL {pilihan_dimensi} DISTRIBUTION MAP')

    st.plotly_chart(fig2, use_container_width=True)

