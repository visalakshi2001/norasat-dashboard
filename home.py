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

        st.dataframe(orbit.T.reset_index().rename(columns={"index": "Orbital Elements"}), hide_index=True, use_container_width=True)


    with cols[1]:

        # cont=st.container(height=200, border=False)
        st.image("results/satellite.png", width=400)
        
        st.subheader("Ground Segment")

        map_df = pd.read_csv("results/groundstation.csv")

        st.dataframe(map_df[["ID","Ground Station Name","Latitude (deg)","Longitude (deg)","Altitude (km)","Antenna Gain (dBi)"]], 
                     use_container_width=True, hide_index=True)
        
        exp = st.expander("Show on Map")
        exp.map(map_df.rename(columns={"Latitude (deg)": "lat", "Longitude (deg)": "lon"}), zoom=1, size="pointsize", height=300)