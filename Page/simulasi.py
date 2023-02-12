import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import json
import plotly.express as px
from shapely.geometry import box
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import pickle
import func

def app():
    st.title('Simulation')

    st.write('On this page you can simulate the calculation of the Adaptive Index based on the percentage of the budget that forms it in the selected area. There are three types of budgets that you can adjust, including the Health Budget, the Waste Budget, and the Environment Budget. Please select the district that you want to simulate in the fields below.')

    indo = pd.read_csv('Nepal Data/Hasil CatBoost.csv', sep=';')

    pil_c1, pil_c2 = st.columns(2)

    with pil_c1:
        pilihan_provinsi = st.selectbox(
            'Select Province.', indo.province.unique(), index=2)

        indo_prov = indo[indo.province == pilihan_provinsi]

        # Pilih Provinsi
        if pilihan_provinsi == 'SEMUA':
            indo_prov = indo
        else:
            indo_prov = indo[indo.province == pilihan_provinsi]
        
    with pil_c2:
        pilihan_kabkota = st.selectbox(
            'Select District.', indo_prov.district.to_list(), index=7)

    
    st.write('---')
    
    # Pilih Kabkota
    if pilihan_kabkota:
        indo_prov = indo_prov[indo_prov.district == pilihan_kabkota].reset_index(drop=True)

        st.subheader('Adaptive Score Prediction')

        st.text('Please enter or change the percentage value for each budget then press the "Prediction" button to see the adaptive score prediction value.')

        c1, c2 = st.columns(2)

        with c1:
            bencana = st.text_input('Disaster Budget (%)', round(indo_prov['Disaster Budget (%)'][0], 4))
            kesehatan = st.text_input('Health Budget (%)', round(indo_prov['Health Budget (%)'][0], 4))
            pangan = st.text_input('Food Budget (%)', round(indo_prov['Food Budget (%)'][0], 4))
            sampah = st.text_input('Garbage Budget (%)', round(indo_prov['Garbage Budget (%)'][0], 4))
            lingkungan_hidup = st.text_input('Environment Budget (%)', round(indo_prov['Environment Budget (%)'][0], 4))

            prediksi_button = st.button('Predictions')
            # reset_button = st.button('Reset')

        with c2:
            # if reset_button:
            #     pyautogui.hotkey("ctrl","F5")

            st.write('')
            st.write('')
            st.write('')

            if prediksi_button:
                list_nilai = [float(bencana), float(kesehatan), float(pangan), float(sampah), float(lingkungan_hidup)]

                # PREDIKSI
                nilai_prediksi = float(func.prediksi_adaptive(list_nilai))

                pred_gauge = go.Figure(go.Indicator(
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    value = round(nilai_prediksi, 4),
                    mode = "gauge+number+delta",
                    title = {'text': "ADAPTIVE SCORE PREDICTION"},
                    delta = {'reference': round(indo_prov['Adaptive Index Pred'][0], 4), 'increasing': {'color': "RebeccaPurple"}},
                    gauge = {'axis': {'range': [0, 100]},
                            'steps' : [
                                {'range': [0, 33], 'color': "#e27e40"},
                                {'range': [33, 66], 'color': "#dfa367"},
                                {'range': [66, 100], 'color': "#debd8a"}],
                            }
                        )
                    )

                pred_gauge.update_layout(
                    height=350,
                    margin=go.layout.Margin(
                        l=50, #left margin
                        r=50, #right margin
                        b=50, #bottom margin
                        t=50  #top margin
                    )
                ) 

                st.plotly_chart(pred_gauge, use_container_width=True)

            else:
                pred_gauge = go.Figure(go.Indicator(
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    value = round(indo_prov['Adaptive Index Pred'][0], 4),
                    mode = "gauge+number",
                    title = {'text': "ADAPTIVE SCORE"},
                    gauge = {'axis': {'range': [0, 100]},
                            'steps' : [
                                {'range': [0, 33], 'color': "#e27e40"},
                                {'range': [33, 66], 'color': "#dfa367"},
                                {'range': [66, 100], 'color': "#debd8a"}],
                            }
                        )
                    )

                pred_gauge.update_layout(
                    height=350,
                    margin=go.layout.Margin(
                        l=50, #left margin
                        r=50, #right margin
                        b=50, #bottom margin
                        t=50  #top margin
                    )
                )

                st.plotly_chart(pred_gauge, use_container_width=True)