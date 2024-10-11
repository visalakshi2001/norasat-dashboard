import streamlit as st
import pandas as pd
import numpy as np

def homefunc():

    cols = st.columns(2)

    with cols[0]:
        cont = st.container(border=True)
        cont.subheader("Mission Overview")

        cont.markdown("""**Mission Name:** NoraSat  
                    **Mission Date:** 01/01/2025 - 01/08/2025""", True)
        
        st.subheader("Orbit Definition")
        orbit = pd.read_csv("results/orbitdetails.csv", index_col=0)

        st.dataframe(orbit.T.reset_index(), hide_index=True)

    with cols[1]:
        cont=st.container(height=200, border=False)
        cont.image("results/satellite.jpg", use_column_width=True)

        st.subheader("Ground Segmentation Definition")

        map_df = pd.read_csv("results/groundstation.csv")

        st.dataframe(map_df[["loc_name", "lat", "lon"]], use_container_width=True, hide_index=True)
        st.map(map_df, zoom=1, size="pointsize", height=300)