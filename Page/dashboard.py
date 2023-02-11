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
    st.title('Nepal CCVI Dashboard')

    st.write('On this page you can see a distribution map of the Vulnerability Index, Adaptive Index, Exposure Index, and Sensitivity Index from the selected provinces. \
          Please select the province, district, and dimensions you want to see in the fields below. You can also see the comparability of the values of each variable in the forming dimensions \
          in the selected region.')


    indo = gpd.read_file('SHP NEPAL/Nepal CCVI/Nepal CCVI.shp')

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
            'Select District.', ['ALL'] + indo_prov.district.to_list())

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
        pilihan_dimensi = st.selectbox('Select Dimension.', ['VULNERABILITY', 'ADAPTIVE', 'EXPOSURE', 'SENSITIVITY'])
        if pilihan_dimensi == 'VULNERABILITY':
            var_dimensi = 'vul_index'
            var_color = 'Haline'
            var_range_color = [1,10]
        elif pilihan_dimensi == 'ADAPTIVE':
            var_dimensi = 'adap_index'
            var_color = 'YlOrBr'
            var_range_color = [0,100]
        elif pilihan_dimensi == 'EXPOSURE':
            var_dimensi = 'expo_index'
            var_color = 'PuBu'
            var_range_color = [0,100]
        elif pilihan_dimensi == 'SENSITIVITY':
            var_dimensi = 'sensi_inde'
            var_color = 'dense'
            var_range_color = [0,100]
    
    st.write('---')

    # 4 Carboard / Metrics
    cn1, cn2, cn3, cn4 = st.columns([1,1,1,1])

    # st.write(indo_prov.dtypes)

    index_rerata = indo_prov[['province', 'expo_index', 'sensi_inde', 'adap_index', 'vul_index']].groupby('province').mean()

    # Metric INDEKS Vulnerabilty
    fig_gauge = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = round(index_rerata.vul_index[0], 3),
        mode = "gauge+number",
        title = {'text': "VULNERABILITY INDEX"},
        gauge = {'axis': {'range': [0, 10]},
                'steps' : [
                    {'range': [0, 4], 'color': "#e27e40"},
                    {'range': [4, 7], 'color': "#dfa367"},
                    {'range': [7, 10], 'color': "#debd8a"}],
                }
            )
        )
    
    fig_gauge.update_layout(
        height=100,
        margin=go.layout.Margin(
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=0  #top margin
        )
    )

    # cn1.subheader('VULNERABILITY INDEX')
    cn1.plotly_chart(fig_gauge, use_container_width=True)
    cn1.markdown("<h5 style='text-align: center; color: black;'>VULNERABILITY INDEX</h1>", unsafe_allow_html=True)

    # Metric INDEKS 1
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_4 = f"""<p style='background-color: #ff7b00; 
                            color: #FAFAFA; 
                            font-size: 34px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:35px;'>
                            {round(index_rerata.adap_index[0], 3)}
                            </style><BR><span style='font-size: 18px; 
                            margin-top: 0;'>ADAPTIVE INDEX</style></span></p>"""

    cn2.markdown(lnk + htmlstr_4, unsafe_allow_html=True)

    # Metric Nilai Target
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_2 = f"""<p style='background-color: #0064b9; 
                            color: #FAFAFA; 
                            font-size: 34px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:35px;'>
                            {round(index_rerata.expo_index[0], 3)}
                            </style><BR><span style='font-size: 18px; 
                            margin-top: 0;'>EXPOSURE INDEX</style></span></p>"""

    cn3.markdown(lnk + htmlstr_2, unsafe_allow_html=True)

    # Metric Nilai Realisasi
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_3 = f"""<p style='background-color: #612798; 
                            color: #FAFAFA; 
                            font-size: 34px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:35px;'>
                            {round(index_rerata.sensi_inde[0], 3)}
                            </style><BR><span style='font-size: 18px; 
                            margin-top: 0;'>SENSITIVITY INDEX</style></span></p>"""

    cn4.markdown(lnk + htmlstr_3, unsafe_allow_html=True)


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
        hover_data={'vul_index':True, 'adap_index':True, 'expo_index':True, 'sensi_inde':True},
        labels={'district':'District', 'vul_index':'Vulnerability Index', 'adap_index':'Adaptive Index', 'expo_index':'Exposure Index', 'sensi_inde':'Sensitivity Index'}
    )
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig2.update_layout({'plot_bgcolor': '#2c2f38', 'paper_bgcolor': '#2c2f38'})

    if len(indo_prov) > 1 and len(indo_prov) < 70:
        st.subheader(f'{pilihan_provinsi} {pilihan_dimensi} INDEX DISTRIBUTION MAP')
    elif len(indo_prov) == 1:
        st.subheader(f'{pilihan_kabkota} - {pilihan_provinsi} {pilihan_dimensi} INDEX DISTRIBUTION MAP')
    else:
        st.subheader(f'NEPAL {pilihan_dimensi} INDEX DISTRIBUTION MAP')

    st.plotly_chart(fig2, use_container_width=True)

