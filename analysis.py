import streamlit as st
import graphviz
import pandas as pd

import plotly.express as px

COLORS = px.colors.qualitative.Plotly

def requirements():
    # Make a heading of size H2
    st.subheader("Requirement Analysis", divider="orange")
    breakdown = pd.read_csv("results/requirements.csv")

    req_choice = st.selectbox("Select Requirement by Name", options=breakdown["ReqName"])
    target_req = breakdown[breakdown["ReqName"] == req_choice]

    dot = graphviz.Digraph(comment='Hierarchy', strict=True)
    for _, row in target_req.iterrows():
            req = row["ReqName"]
            verified = row["VerifiedBy"]
            satisfied = row["SatisfiedBy"]
            result = row["Results"]
            status = row["VerificationStatus"]

            if pd.notna(req):
                dot.node(req)

            if pd.notna(verified):
                if verified not in dot.body:
                    dot.node(verified)
                dot.edge(req, verified, label="verified by")
            
            if pd.notna(satisfied):
                if satisfied not in dot.body:
                    dot.node(satisfied)
                dot.edge(req, satisfied, label="satisfied by")
            if pd.notna(result):
                if result not in dot.body:
                    dot.node(result)
                dot.edge(verified, result, label="analysis output")
            
            if pd.notna(status):
                if status not in dot.body:
                    dot.node(status, shape="box")
                dot.edge(result, status, label="verification status")
            
    cols = st.columns([0.35, 0.5])
    cols[0].graphviz_chart(dot, True)

    cols[1].dataframe(target_req.rename({0: "values", 1: "values", 2: "values"}).T, use_container_width=True)

    showdata = cols[1].checkbox("Show all requirements data")

    if showdata:
        cols[1].dataframe(breakdown.set_index("ReqID"))



def results():

    calc = pd.read_csv("results/calculation.csv")

    st.subheader("Results", divider="green")
    analysis_opts = ["Sedaro Analysis", "SNR Calculations"]
    analysis = st.selectbox("Select Analysis", options=analysis_opts)

    cols = st.columns(2)

    target_analysis = calc[calc["Analysis Name"] == analysis]
    if analysis == analysis_opts[0]:
        with cols[0]:
            cont = st.container(border=True)
            cont.subheader("Analysis Overview")
            cont.dataframe(target_analysis.set_index("Analysis Name"), use_container_width=True)
        
        with cols[1]:
            cont = st.container(border=True)
            cont.subheader("Visualizations")
            cont.write("If any applicable")

            viz_opts = target_analysis["Outputs"].unique()
            viz = cont.radio("Select Output", options=viz_opts, horizontal=True)

            viz_table = target_analysis[target_analysis["Outputs"] == viz]
            if viz == viz_opts[0]:
                fig = px.bar(viz_table, x="Inputs", y="Results", text="Results", title="Total Access time")
                fig.update_traces(marker_color=COLORS[3], textposition="outside")
                cont.plotly_chart(fig, True)

            if viz == viz_opts[1]:
                cont.markdown("**Max Range**")
                for i,row in viz_table.iterrows():
                    value = str(row["Results"]) + " " + str(row["Unit"]) if row["Unit"] else str(row["Results"])
                    delta = str(row["Verification Status"])
                    deltacolor = "normal" if delta == "PASS" else "inverse"
                    cont.metric(label=row["Inputs"], value=value, delta=delta, delta_color=deltacolor)

    cols = st.columns(2)
    if analysis == analysis_opts[1]:
        with cols[0]:
            cont = st.container(border=True)
            cont.subheader("Analysis Overview")
            cont.dataframe(target_analysis.set_index("Analysis Name"), use_container_width=True)
        
        with cols[1]:
            cont = st.container(border=True)
            cont.subheader("Visualizations")
            cont.write("If any applicable")

