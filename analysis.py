import streamlit as st
import graphviz
import pandas as pd

import plotly.express as px

COLORS = px.colors.qualitative.Plotly
more_colors = {
    "green": "#4bde9c",
    "red": "#fb8072",
    "amber": "#ffed6f"
}

def requirements():

    st.subheader("Requirements Summary", divider="orange")
    breakdown = pd.read_csv("results/requirements.csv")

    cols = st.columns([0.7,0.15])

    cols[0].dataframe(breakdown.drop(columns=["Results"]).set_index("Requirement Name").style. \
                 applymap(lambda x: f'background-color: {more_colors["green"]}' if x == "PASS" \
                           else (
                               f'background-color: {more_colors["red"]}' if x == "FAIL"   
                               else f'background-color: {more_colors["amber"]}'
                           ), 
                          subset=["Verification Status"]), 
                 use_container_width=True)
    
    cont = cols[1].container(border=True)
    cont.subheader("Warnings")
    for _, row in breakdown.iterrows():
        req = row["Requirement Name"]
        verified = row["Verified By"]
        satisfied = row["Satisfied By"]
        result = row["Results"]
        status = row["Verification Status"]

        if pd.isna(verified):
            cont.warning(f"Requirement {req} is not verified by any analysis", icon="⚠️")
        if pd.isna(satisfied):
            cont.warning(f"Requirement {req} is not satisfied by any mission element", icon="⚠️")
        if pd.notna(verified) and status != "PASS":
            cont.error(f"Requirement {req} has not PASSED the analysis")

    req_choice = st.selectbox("Select Requirement by Name", options=breakdown["Requirement Name"], index=1)
    target_req = breakdown[breakdown["Requirement Name"] == req_choice]

    dot = graphviz.Digraph(comment='Hierarchy', strict=True)
    for _, row in target_req.iterrows():
            req = row["Requirement Name"]
            verified = row["Verified By"]
            satisfied = row["Satisfied By"]
            result = row["Results"]
            status = row["Verification Status"]

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
            
            if pd.notna(result) and pd.notna(status):
                if status not in dot.body:
                    dot.node(status, shape="box")
                dot.edge(result, status, label="verification status")
            
    cols = st.columns([0.23 ,0.5])
    cols[0].graphviz_chart(dot, True)

    cols[-1].dataframe(target_req.rename({0: "values", 1: "values", 2: "values", 3: "values", 4: "values"}).T, use_container_width=True)

    # with cols[1]:
    #     cont = st.container(border=True)
    #     cont.subheader("Warnings")
    #     for _, row in target_req.iterrows():
    #         req = row["Requirement Name"]
    #         verified = row["Verified By"]
    #         satisfied = row["Satisfied By"]
    #         result = row["Results"]
    #         status = row["Verification Status"]

    #         if pd.isna(verified):
    #             cont.warning(f"Requirement {req} is not verified by any analysis", icon="⚠️")
    #         if pd.isna(satisfied):
    #             cont.warning(f"Requirement {req} is not satisfied by any mission element", icon="⚠️")
    #         if pd.notna(verified) and status != "PASS":
    #             cont.error(f"Requirement {req} has not PASSED the analysis")

    #         if pd.notna(verified) and pd.notna(satisfied) and pd.notna(status) and status == "PASS":
    #             cont.info(f"{req} requirement has no warnings/issues")





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
            cont.markdown(f"**Analysis Name:** {analysis}", True)
            cont.dataframe(target_analysis.drop(columns=["Analysis Name", "Mission Element", "OutputName"]).set_index("Analysis Tool"), use_container_width=True)
        
        with cols[1]:
            cont = st.container(border=True)
            cont.subheader("Visualizations")
            cont.caption("If any applicable")

            viz_opts = target_analysis["OutputName"].unique()
            viz = cont.radio("Select Output", options=viz_opts, horizontal=True)

            viz_table = target_analysis[target_analysis["OutputName"] == viz]
            if viz == viz_opts[0]:
                fig = px.bar(viz_table, x="Mission Element", y="Results", color="Mission Element",
                             color_discrete_map=dict(zip(viz_table["Mission Element"], 
                                                         [COLORS[1] if bar=="Total" else COLORS[3] for bar in viz_table["Mission Element"]])),
                             text="Results", title="Average Daily Access Time")
                fig.update_traces(textposition="outside", showlegend=False)
                fig.update_layout(yaxis_title="Total Time (s)")
                cont.plotly_chart(fig, True)
           
            if viz == viz_opts[1]:
                cont.markdown("**Max Range**")
                for i,row in viz_table.iterrows():
                    value = str(row["Results"]) + " " + str(row["Unit"]) if row["Unit"] else str(row["Results"])
                    delta = str(row["Verification Status"])
                    deltacolor = "normal" if delta == "PASS" else "inverse"
                    cont.metric(label=row["Mission Element"], value=value, delta=delta, delta_color=deltacolor)

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

