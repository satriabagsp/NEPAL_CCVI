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
    st.title('Simulasi')

    st.write('Pada halaman ini anda dapat melakukan simulasi penghitungan Adapative Index berdasarkan persentase anggaran pembentuknya di wilayah yang dipilih. Terdapat tiga tipe anggaran yang dapat \
        anda sesuaikan, antara lain Anggaran Kesehatan, Anggaran Sampah, dan Anggaran Lingkungan Hidup. Silakan pilih kabupaten/kota yang ingin anda simulasikan pada isian di bawah.')

    indo = pd.read_csv('Data/Hasil Cat Boost.csv', sep=';')

    pil_c1, pil_c2 = st.columns(2)

    with pil_c1:
        pilihan_provinsi = st.selectbox(
            'Pilih Provinsi.', indo.nmprov.unique(), index=10)

        indo_prov = indo[indo.nmprov == pilihan_provinsi]

        # Pilih Provinsi
        if pilihan_provinsi == 'SEMUA':
            indo_prov = indo
        else:
            indo_prov = indo[indo.nmprov == pilihan_provinsi]
        
    with pil_c2:
        pilihan_kabkota = st.selectbox(
            'Pilih Kabupaten/kota.', indo_prov.nmkab.to_list())

    
    st.write('---')
    
    # Pilih Kabkota
    if pilihan_kabkota:
        indo_prov = indo_prov[indo_prov.nmkab == pilihan_kabkota].reset_index(drop=True)

        st.subheader('Prediksi Adaptive Score')

        st.text('Silakan isikan atau ubah nilai persentase masing-masing anggaran kemudian tekan tombol "Prediksi" untuk melihat nilai prediksi skor adaptif.')

        c1, c2 = st.columns(2)

        with c1:
            # bencana = st.text_input('Persentase Anggaran Bencana (%)', round(indo_prov.persen_anggaran_bencana[0], 4))
            kesehatan = st.text_input('Persentase Anggaran Kesehatan (%)', round(indo_prov.persen_anggaran_kesehatan[0], 4))
            # pangan = st.text_input('Persentase Anggaran Pangan (%)', round(indo_prov.persen_anggaran_pangan[0], 4))
            sampah = st.text_input('Persentase Anggaran Sampah (%)', round(indo_prov.persen_anggaran_sampah[0], 4))
            lingkungan_hidup = st.text_input('Persentase Anggaran Lingkungan Hidup (%)', round(indo_prov.persen_anggaran_lh[0], 4))

            prediksi_button = st.button('Prediksi')
            # reset_button = st.button('Reset')

        with c2:
            # if reset_button:
            #     pyautogui.hotkey("ctrl","F5")

            if prediksi_button:
                list_nilai = [float(kesehatan), float(sampah), float(lingkungan_hidup)]

                # PREDIKSI
                nilai_prediksi = float(func.prediksi_adaptive(list_nilai))

                pred_gauge = go.Figure(go.Indicator(
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    value = round(nilai_prediksi, 4),
                    mode = "gauge+number+delta",
                    title = {'text': "PREDIKSI ADAPTIVE SCORE"},
                    delta = {'reference': round(indo_prov.adap_score_hat[0], 4), 'increasing': {'color': "RebeccaPurple"}},
                    gauge = {'axis': {'range': [0, 100]},
                            'steps' : [
                                {'range': [0, 33], 'color': "#e27e40"},
                                {'range': [33, 66], 'color': "#dfa367"},
                                {'range': [66, 100], 'color': "#debd8a"}],
                            }
                        )
                    )

                pred_gauge.update_layout(
                    height=300,
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
                    value = round(indo_prov.adap_score_hat[0], 4),
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
                    height=300,
                    margin=go.layout.Margin(
                        l=50, #left margin
                        r=50, #right margin
                        b=50, #bottom margin
                        t=50  #top margin
                    )
                )

                st.plotly_chart(pred_gauge, use_container_width=True)