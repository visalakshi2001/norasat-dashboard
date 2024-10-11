import streamlit as st
import pandas as pd
import graphviz


def archfunc():
    system = pd.read_csv("results/systems.csv")
    mission = pd.read_csv("results/missions.csv")
    transmitter = pd.read_csv("results/transmittertradeoff.csv")

    viewlist = ["System Architecture", "Mission", "Transmitter Trade-Off"]
    view = st.selectbox("Select View", options=viewlist)

    dot = graphviz.Digraph(comment='Hierarchy', strict=True)
    cols = st.columns([0.7, 0.3])
    if view == viewlist[0]:
        for _, row in system.iterrows():
                sys = row["System"]
                subsys = row["Subsystem"]

                if pd.notna(sys):
                    dot.node(sys)

                if pd.notna(subsys):
                    if subsys not in dot.body:
                        dot.node(subsys)
                    dot.edge(sys, subsys, label="has subsystem")
        cols[0].graphviz_chart(dot, True)
    
    if view == viewlist[1]:
        for _, row in mission.iterrows():
                miss = row["MissionName"]
                sys = row["SystemName"]
                comp = row["MissionComponent"]

                if pd.notna(miss):
                    dot.node(miss)

                if pd.notna(sys):
                    dot.edge(miss, sys, label="has system")
                
                if pd.notna(comp):
                    dot.edge(sys, comp, label="has mission component")
        cols[0].graphviz_chart(dot, True)
    
    if view == viewlist[2]:
         st.dataframe(transmitter, hide_index=True, use_container_width=True)