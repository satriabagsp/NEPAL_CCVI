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
    st.title('Dimensi per Kabupaten/kota')

    st.write('Pada halaman ini anda dapat melihat nilai variabel dari dimensi-dimensi pembentuk Vulnerability Index. Silakan pilih provinsi, kabupaten/kota, dan dimensi yang \
        ingin anda lihat. Anda juga dapat melihat perbanding dari dua wilayah kabupaten/kota dengan mengisikan pilihan kabupaten/kota pembanding.')

    st.write('---')

    indo = gpd.read_file('SHP KABUPATEN INDONESIA/Merge/result.shp')

    pil_c1, pil_c2 = st.columns(2)

    with pil_c1:
        # Pilih Provinsi
        pilihan_provinsi = st.selectbox(
            'Pilih Provinsi:',
            ['ACEH','SUMATERA UTARA','SUMATERA BARAT','RIAU','JAMBI','SUMATERA SELATAN','BENGKULU','LAMPUNG',
                'KEPULAUAN BANGKA BELITUNG','KEPULAUAN RIAU','DKI JAKARTA','JAWA BARAT','JAWA TENGAH','DI YOGYAKARTA','JAWA TIMUR',
                'BANTEN','BALI','NUSA TENGGARA BARAT','NUSA TENGGARA TIMUR','KALIMANTAN BARAT','KALIMANTAN TENGAH','KALIMANTAN SELATAN',
                'KALIMANTAN TIMUR','KALIMANTAN UTARA','SULAWESI UTARA','SULAWESI TENGAH','SULAWESI SELATAN','SULAWESI TENGGARA','GORONTALO',
                'SULAWESI BARAT','MALUKU','MALUKU UTARA','PAPUA BARAT','PAPUA'],
            index=11)

        indo_prov = indo[indo.nmprov == pilihan_provinsi]

        pilihan_kabkota = st.selectbox(
            'Pilih Kabupaten/kota:', indo_prov.nmkab.to_list())

        pilihan_kabkota_pembanding = st.selectbox(
            'Pilih Kabupaten/kota Pembanding (Opsional):', ['-'] + indo_prov.nmkab.to_list())

        # Pilih Kabkota
        indo_prov_pil = indo_prov[indo_prov.nmkab == pilihan_kabkota]
        indo_prov_pembanding = indo_prov[indo_prov.nmkab == pilihan_kabkota_pembanding]
        df_kabkota = indo_prov_pil[['idkab','nmkab']].drop_duplicates()
        df_kabkota_pembanding = indo_prov_pembanding[['idkab','nmkab']].drop_duplicates()

        # Pilih Dimensi
        pilihan_dimensi = st.selectbox('Pilih Dimensi:', ['ADAPTIVE', 'EXPOSURE', 'SENSITIVITY'])
        if pilihan_dimensi == 'ADAPTIVE':
            # DF Origin
            dimensi_adaptive = pd.read_csv('Data/Variabel/adaptivity_data.csv')
            dimensi_adaptive = dimensi_adaptive.merge(df_kabkota, left_on='kab_code', right_on='idkab',  how='right').reset_index(drop=True)

            # DF Pembanding
            dimensi_adaptive_pembanding = pd.read_csv('Data/Variabel/adaptivity_data.csv')
            dimensi_adaptive_pembanding = dimensi_adaptive_pembanding.merge(df_kabkota_pembanding, left_on='kab_code', right_on='idkab',  how='right').reset_index(drop=True)


            # Dropdown aspek
            aspek = pd.read_csv('Data/Variabel/metadata variabel podes.csv', sep=';')
            pilihan_aspek = st.selectbox('Pilih Aspek:', aspek.aspek.unique(), index=3)

            # Filter berdasarkan Aspek
            fil_aspek = aspek[aspek['aspek'] == pilihan_aspek].variabel_code.to_list()
            dimensi_adaptive = dimensi_adaptive[['idkab', 'nmkab'] + fil_aspek]
            dimensi_adaptive_pembanding = dimensi_adaptive_pembanding[['idkab', 'nmkab'] + fil_aspek]
            
            # Ganti Kolom
            dimensi_adaptive = dimensi_adaptive.rename(columns={
                                            'persen_desa_akses':'Desa dengan Akses Jalan Darat (%)',
                                            'persen_desa_jenis_jln':'Desa dengan Jenis Jalan Beton/Aspal (%)',
                                            'persen_desa_kondisi':'Desa dengan Jalan dapat Dilalui Sepanjang Tahun oleh Roda 4 (%)',
                                            'more_sma':'Penduduk dengan Ijazah SMA ke Atas (%)',
                                            'yes_working':'Penduduk yang Bekerja di Pertanian (%)',
                                            'own_tel_rumah':'Rumah Tangga yang Memiliki Telepon Rumah (%)',
                                            'persen_kec_puskes_kumham':'Kecamatan dengan Puskesmas > 1:16.000 (%)',
                                            'persen_puskespem_kumham':'Desa dengan Puskesmas Pembantu > 1:1500 (%)',
                                            'persen_faskes_kumham':'Desa dengan Fasilitas Kesehatan > 1:1500 (%)',
                                            'persen_desa_dokter_kumham':'Desa dengan Rasio Dokter > 1:2500 Populasi (%)',
                                            'persen_desa_nakes_kumham':'Desa dengan Rasio Tenaga Kesehatan > 1:855 Populasi (%)',
                                            'persen_desa_bidan_kumham':'Desa dengan Rasio Bidan > 1:1000 Populasi (%)',
                                            'own_asuransi':'Penduduk yang Memiliki Asuransi (%)',
                                            'yes_norek':'Penduduk yang Memiliki Nomor Rekening (%)',
                                            'ada_kredit':'Rumah Tangga yang Memiliki Kredit (%)',
                                            'persen_desa_bankpem':'Desa yang Memiliki Bank Pemerintah (%)',
                                            'persen_desa_bankswasta':'Desa yang Memiliki Bank Swasta (%)',
                                            'persen_desa_mitigasi':'Desa yang Memiliki Mitigasi Bencana (%)',
                                            'use_inet':'Penduduk Pengguna Internet (%)',
                                            'own_ponsel':'Penduduk yang Memiliki Ponsel (%)',
                                            'persen_desa_internet':'Desa dengan Internet untuk Warnet dan Fasilitas Umum (%)',
                                            'persen_desa_sinyal':'Desa dengan Internet 3G atau Lebih (%)'
                                        })
            dimensi_adaptive_pembanding = dimensi_adaptive_pembanding.rename(columns={
                                            'persen_desa_akses':'Desa dengan Akses Jalan Darat (%)',
                                            'persen_desa_jenis_jln':'Desa dengan Jenis Jalan Beton/Aspal (%)',
                                            'persen_desa_kondisi':'Desa dengan Jalan dapat Dilalui Sepanjang Tahun oleh Roda 4 (%)',
                                            'more_sma':'Penduduk dengan Ijazah SMA ke Atas (%)',
                                            'yes_working':'Penduduk yang Bekerja di Pertanian (%)',
                                            'own_tel_rumah':'Rumah Tangga yang Memiliki Telepon Rumah (%)',
                                            'persen_kec_puskes_kumham':'Kecamatan dengan Puskesmas > 1:16.000 (%)',
                                            'persen_puskespem_kumham':'Desa dengan Puskesmas Pembantu > 1:1500 (%)',
                                            'persen_faskes_kumham':'Desa dengan Fasilitas Kesehatan > 1:1500 (%)',
                                            'persen_desa_dokter_kumham':'Desa dengan Rasio Dokter > 1:2500 Populasi (%)',
                                            'persen_desa_nakes_kumham':'Desa dengan Rasio Tenaga Kesehatan > 1:855 Populasi (%)',
                                            'persen_desa_bidan_kumham':'Desa dengan Rasio Bidan > 1:1000 Populasi (%)',
                                            'own_asuransi':'Penduduk yang Memiliki Asuransi (%)',
                                            'yes_norek':'Penduduk yang Memiliki Nomor Rekening (%)',
                                            'ada_kredit':'Rumah Tangga yang Memiliki Kredit (%)',
                                            'persen_desa_bankpem':'Desa yang Memiliki Bank Pemerintah (%)',
                                            'persen_desa_bankswasta':'Desa yang Memiliki Bank Swasta (%)',
                                            'persen_desa_mitigasi':'Desa yang Memiliki Mitigasi Bencana (%)',
                                            'use_inet':'Penduduk Pengguna Internet (%)',
                                            'own_ponsel':'Penduduk yang Memiliki Ponsel (%)',
                                            'persen_desa_internet':'Desa dengan Internet untuk Warnet dan Fasilitas Umum (%)',
                                            'persen_desa_sinyal':'Desa dengan Internet 3G atau Lebih (%)'
                                        })
            
            # Melt Origin
            dimensi_adaptive.pop('idkab')
            dimensi_adaptive = dimensi_adaptive.melt(id_vars=['nmkab'])
            
            # Melt Pembanding
            dimensi_adaptive_pembanding.pop('idkab')
            dimensi_adaptive_pembanding = dimensi_adaptive_pembanding.melt(id_vars=['nmkab'])

            with pil_c2:
                # Plot Spider
                fig_spider = go.Figure(data=go.Scatterpolar(
                    r = dimensi_adaptive['value'],
                    theta = dimensi_adaptive['variable'],
                    fill='toself',
                    name = str(dimensi_adaptive['nmkab'][0])
                ))
                if len(dimensi_adaptive_pembanding) != 0:
                    fig_spider.add_trace(go.Scatterpolar(
                        r = dimensi_adaptive_pembanding['value'],
                        theta = dimensi_adaptive_pembanding['variable'],
                        fill ='toself',
                        name = str(dimensi_adaptive_pembanding['nmkab'][0])
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
            dimensi_exposure = pd.read_csv('Data/Variabel/exposure_data.csv')
            dimensi_exposure = dimensi_exposure.merge(df_kabkota, left_on='kab_code', right_on='idkab',  how='right').reset_index(drop=True)
            dimensi_exposure = dimensi_exposure.rename(columns={'longsor_per_year':'Longsor','banjir_per_year':'Banjir','ekstrim_per_year':'Cuaca Ekstrim','kekeringan_per_year':'Kekeringan'})
           
            # Df pembanding
            dimensi_exposure_pembanding = pd.read_csv('Data/Variabel/exposure_data.csv')
            dimensi_exposure_pembanding = dimensi_exposure_pembanding.merge(df_kabkota_pembanding, left_on='kab_code', right_on='idkab',  how='right').reset_index(drop=True)
            dimensi_exposure_pembanding = dimensi_exposure_pembanding.rename(columns={'longsor_per_year':'Longsor','banjir_per_year':'Banjir','ekstrim_per_year':'Cuaca Ekstrim','kekeringan_per_year':'Kekeringan'})

            # Melt
            dimensi_exposure.pop('kab_code')
            dimensi_exposure.pop('idkab')
            dimensi_exposure = dimensi_exposure.melt(id_vars=['nmkab'])

            # Melt Pembanding
            dimensi_exposure_pembanding.pop('kab_code')
            dimensi_exposure_pembanding.pop('idkab')
            dimensi_exposure_pembanding = dimensi_exposure_pembanding.melt(id_vars=['nmkab'])

            with pil_c2:
                # Plot Spider
                fig_spider = go.Figure(data=go.Scatterpolar(
                    r = dimensi_exposure['value'],
                    theta = dimensi_exposure['variable'],
                    fill='toself',
                    name = str(dimensi_exposure['nmkab'][0])
                ))
                if len(dimensi_exposure_pembanding) != 0:
                    fig_spider.add_trace(go.Scatterpolar(
                        r = dimensi_exposure_pembanding['value'],
                        theta = dimensi_exposure_pembanding['variable'],
                        fill ='toself',
                        name = str(dimensi_exposure_pembanding['nmkab'][0])
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
            dimensi_sensitivity = pd.read_csv('Data/Variabel/sensitivity_data.csv')
            dimensi_sensitivity = dimensi_sensitivity.merge(df_kabkota, left_on='kab_code', right_on='idkab',  how='right').reset_index(drop=True)
            dimensi_sensitivity = dimensi_sensitivity.rename(columns={
                                        'balita':'Penduduk Balita (%)',
                                        'lansia':'Penduduk Lansia (%)',
                                        'pertanian':'Penduduk Pekerja Pertanian (%)',
                                        'merokok':'Penduduk Perokok Aktif (%)',
                                        'no_access_food':'Rumah Tangga Tanpa Akses ke Makanan (%)',
                                        'hunian_tak_layak':'Rumah Tangga dengan Hunian Tidak Layak (%)',
                                        'persen_desa_laut':'Desa yang Berbatasan dengan Laut (%)',
                                        'persen_kel_sungai':'Keluarga yang Tinggal di Bantaran Sungai (%)',
                                        'persen_disabilitas':'Penduduk Disabilitas (%)'})

            # Df pembanding
            dimensi_sensitivity_pembanding = pd.read_csv('Data/Variabel/sensitivity_data.csv')
            dimensi_sensitivity_pembanding = dimensi_sensitivity_pembanding.merge(df_kabkota_pembanding, left_on='kab_code', right_on='idkab',  how='right').reset_index(drop=True)
            dimensi_sensitivity_pembanding = dimensi_sensitivity_pembanding.rename(columns={
                                        'balita':'Penduduk Balita (%)',
                                        'lansia':'Penduduk Lansia (%)',
                                        'pertanian':'Penduduk Pekerja Pertanian (%)',
                                        'merokok':'Penduduk Perokok Aktif (%)',
                                        'no_access_food':'Rumah Tangga Tanpa Akses ke Makanan (%)',
                                        'hunian_tak_layak':'Rumah Tangga dengan Hunian Tidak Layak (%)',
                                        'persen_desa_laut':'Desa yang Berbatasan dengan Laut (%)',
                                        'persen_kel_sungai':'Keluarga yang Tinggal di Bantaran Sungai (%)',
                                        'persen_disabilitas':'Penduduk Disabilitas (%)'})

            # Melt
            dimensi_sensitivity.pop('kab_code')
            dimensi_sensitivity.pop('idkab')
            dimensi_sensitivity = dimensi_sensitivity.melt(id_vars=['nmkab'])

            # Melt Sensitivity
            dimensi_sensitivity_pembanding.pop('kab_code')
            dimensi_sensitivity_pembanding.pop('idkab')
            dimensi_sensitivity_pembanding = dimensi_sensitivity_pembanding.melt(id_vars=['nmkab'])

            with pil_c2:
                # Plot Spider
                fig_spider = go.Figure(data=go.Scatterpolar(
                    r = dimensi_sensitivity['value'],
                    theta = dimensi_sensitivity['variable'],
                    fill='toself',
                    name = str(dimensi_sensitivity['nmkab'][0])
                ))
                if len(dimensi_sensitivity_pembanding) != 0:
                    fig_spider.add_trace(go.Scatterpolar(
                        r = dimensi_sensitivity_pembanding['value'],
                        theta = dimensi_sensitivity_pembanding['variable'],
                        fill ='toself',
                        name = str(dimensi_sensitivity_pembanding['nmkab'][0])
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
