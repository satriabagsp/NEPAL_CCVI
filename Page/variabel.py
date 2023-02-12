import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import json
import plotly.express as px
from shapely.geometry import box
import plotly.graph_objects as go
import func
import geopandas as gpd

def app():
    st.title('Dimension per District')

    st.write('On this page you can see the variable values of the dimensions that make up the Vulnerability Index. Please select the desired province, district and dimensions \
         you want to see. You can also see a comparison of the two districts by filling in the options for the comparison district.')

    st.write('---')

    indo = gpd.read_file('SHP NEPAL/Nepal CCVI/Nepal CCVI.shp')

    pil_c1, pil_c2 = st.columns(2)

    with pil_c1:
        # Pilih Provinsi
        pilihan_provinsi = st.selectbox(
            'Select Province:',
            ['1', '2', 'BAGMATI', 'KARNALI', '5', 'SUDUR PASHCHIM', 'GANDAKI'],
            index=2)

        indo_prov = indo[indo.province == pilihan_provinsi]

        pilihan_kabkota = st.selectbox(
            'Select District:', indo_prov.district.to_list())

        pilihan_kabkota_pembanding = st.selectbox(
            'Select Comparison District (Optional):', ['-'] + indo_prov.district.to_list())


        # Pilih Dimensi
        pilihan_dimensi = st.selectbox('Select Dimension:', ['ADAPTIVE', 'EXPOSURE', 'SENSITIVITY'])
        if pilihan_dimensi == 'ADAPTIVE':
            # DF Origin
            dimensi_adaptive = pd.read_csv('Nepal Data\Variable\ADAPTIVITY.csv')
            dimensi_adaptive = dimensi_adaptive[dimensi_adaptive['district'] == pilihan_kabkota.title()]

            # DF Pembanding
            dimensi_adaptive_pembanding = pd.read_csv('Nepal Data\Variable\ADAPTIVITY.csv')
            dimensi_adaptive_pembanding = dimensi_adaptive_pembanding[dimensi_adaptive_pembanding['district'] == pilihan_kabkota_pembanding.title()]

            # Melt
            dimensi_adaptive.pop('province')
            dimensi_adaptive = dimensi_adaptive.melt(id_vars=['district'])
            dimensi_adaptive = dimensi_adaptive.dropna()

            # Melt Pembanding
            dimensi_adaptive_pembanding.pop('province')
            dimensi_adaptive_pembanding = dimensi_adaptive_pembanding.melt(id_vars=['district'])
            dimensi_adaptive_pembanding = dimensi_adaptive_pembanding.dropna()

            with pil_c2:
                # Plot Spider
                fig_spider = go.Figure(data=go.Scatterpolar(
                    r = dimensi_adaptive['value'],
                    theta = dimensi_adaptive['variable'],
                    fill='toself',
                    name = pilihan_kabkota
                ))
                if len(dimensi_adaptive_pembanding) != 0:
                    fig_spider.add_trace(go.Scatterpolar(
                        r = dimensi_adaptive_pembanding['value'],
                        theta = dimensi_adaptive_pembanding['variable'],
                        fill ='toself',
                        name = pilihan_kabkota_pembanding
                    ))

                fig_spider.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True
                    ),
                ),
                showlegend=False
                )
                fig_spider.update_layout(
                    height=350,
                    margin=go.layout.Margin(
                        t=40  #top margin
                    )
                ) 
                st.write('')

                st.plotly_chart(fig_spider, use_container_width=True)


        elif pilihan_dimensi == 'EXPOSURE':
            dimensi_exposure = pd.read_csv('Nepal Data/Variable/EXPOSURE.csv')
            dimensi_exposure = dimensi_exposure[dimensi_exposure['district'] == pilihan_kabkota.title()]
            # dimensi_exposure = dimensi_exposure.rename(columns={'longsor_per_year':'Longsor','banjir_per_year':'Banjir','ekstrim_per_year':'Cuaca Ekstrim','kekeringan_per_year':'Kekeringan'})
           
            # Df pembanding
            dimensi_exposure_pembanding = pd.read_csv('Nepal Data/Variable/EXPOSURE.csv')
            dimensi_exposure_pembanding = dimensi_exposure_pembanding[dimensi_exposure_pembanding['district'] == pilihan_kabkota_pembanding.title()]
            # dimensi_exposure_pembanding = dimensi_exposure_pembanding.rename(columns={'longsor_per_year':'Longsor','banjir_per_year':'Banjir','ekstrim_per_year':'Cuaca Ekstrim','kekeringan_per_year':'Kekeringan'})

            # Melt
            dimensi_exposure.pop('province')
            dimensi_exposure = dimensi_exposure.melt(id_vars=['district'])
            dimensi_exposure = dimensi_exposure.dropna()

            # Melt Pembanding
            dimensi_exposure_pembanding.pop('province')
            dimensi_exposure_pembanding = dimensi_exposure_pembanding.melt(id_vars=['district'])
            dimensi_exposure_pembanding = dimensi_exposure_pembanding.dropna()

            with pil_c2:
                # Plot Spider
                fig_spider = go.Figure(data=go.Scatterpolar(
                    r = dimensi_exposure['value'],
                    theta = dimensi_exposure['variable'],
                    fill='toself',
                    name = pilihan_kabkota
                ))
                if len(dimensi_exposure_pembanding) != 0:
                    fig_spider.add_trace(go.Scatterpolar(
                        r = dimensi_exposure_pembanding['value'],
                        theta = dimensi_exposure_pembanding['variable'],
                        fill ='toself',
                        name = pilihan_kabkota_pembanding
                    ))

                fig_spider.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True
                    ),
                ),
                showlegend=False
                )
                fig_spider.update_layout(
                    height=350,
                    margin=go.layout.Margin(
                        t=40  #top margin
                    )
                ) 
                st.write('')

                st.plotly_chart(fig_spider, use_container_width=True)

        elif pilihan_dimensi == 'SENSITIVITY':
            # DF Origin
            dimensi_sensitivity = pd.read_csv('Nepal Data/Variable/SENSITIVITY.csv')
            dimensi_sensitivity = dimensi_sensitivity[dimensi_sensitivity['district'] == pilihan_kabkota.title()]

            # Df pembanding
            dimensi_sensitivity_pembanding = pd.read_csv('Nepal Data/Variable/SENSITIVITY.csv')
            dimensi_sensitivity_pembanding = dimensi_sensitivity_pembanding[dimensi_sensitivity_pembanding['district'] == pilihan_kabkota_pembanding.title()]

            # Melt
            dimensi_sensitivity.pop('province')
            dimensi_sensitivity = dimensi_sensitivity.melt(id_vars=['district'])
            dimensi_sensitivity = dimensi_sensitivity.dropna()

            # Melt Sensitivity
            dimensi_sensitivity_pembanding.pop('province')
            dimensi_sensitivity_pembanding = dimensi_sensitivity_pembanding.melt(id_vars=['district'])
            dimensi_sensitivity_pembanding = dimensi_sensitivity_pembanding.dropna()

            with pil_c2:
                # Plot Spider
                fig_spider = go.Figure(data=go.Scatterpolar(
                    r = dimensi_sensitivity['value'],
                    theta = dimensi_sensitivity['variable'],
                    fill='toself',
                    name = pilihan_kabkota
                ))
                if len(dimensi_sensitivity_pembanding) != 0:
                    fig_spider.add_trace(go.Scatterpolar(
                        r = dimensi_sensitivity_pembanding['value'],
                        theta = dimensi_sensitivity_pembanding['variable'],
                        fill ='toself',
                        name = pilihan_kabkota_pembanding
                    ))

                fig_spider.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True
                    ),
                ),
                showlegend=False
                )
                fig_spider.update_layout(
                    height=350,
                    margin=go.layout.Margin(
                        t=40  #top margin
                    )
                ) 
                st.write('')
                st.plotly_chart(fig_spider, use_container_width=True)
