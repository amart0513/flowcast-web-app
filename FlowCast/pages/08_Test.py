import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="FlowCast: Dropdown Navigation", layout="wide", page_icon="🌊")

# Custom CSS for consistent styling
st.markdown(
    """
    <style>
        /* Banner Styling */
        .hero-title {
            font-size: 3rem;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(135deg, #005f73, #0a9396);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Subheader Styling */
        .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73;
            margin-bottom: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Banner Title
st.markdown('<div class="hero-title">FlowCast: Dropdown Navigation Example</div>', unsafe_allow_html=True)

# Dropdown for Primary Section
primary_section = st.selectbox(
    "Select Analysis Section",
    ["Data Analysis", "Predictive Analysis"],
    help="Choose the primary section to explore.",
)

if primary_section == "Data Analysis":
    st.markdown('<p class="styled-subheader">Data Analysis Section</p>', unsafe_allow_html=True)

    # Nested Tabs for Data Analysis
    analysis_tabs = st.tabs(["Overview", "Visualizations", "Statistics"])
    with analysis_tabs[0]:
        st.write("This is the **Overview** of Data Analysis.")
        st.write("Add content about the dataset, structure, or insights here.")
    with analysis_tabs[1]:
        st.write("This tab contains **Visualizations**.")
        st.write("Add scatter plots, line plots, or other visualizations here.")
    with analysis_tabs[2]:
        st.write("This tab contains **Statistics**.")
        st.write("Add descriptive statistics or correlation analysis here.")

elif primary_section == "Predictive Analysis":
    st.markdown('<p class="styled-subheader">Predictive Analysis Section</p>', unsafe_allow_html=True)

    # Nested Tabs for Predictive Analysis
    prediction_tabs = st.tabs(["Risk Analysis", "Model Performance", "Insights"])
    with prediction_tabs[0]:
        st.write("This tab covers **Risk Analysis**.")
        st.write("Add risk metrics and thresholds for predictions here.")
    with prediction_tabs[1]:
        st.write("This tab covers **Model Performance**.")
        st.write("Add metrics like accuracy, precision, recall, or MSE here.")
    with prediction_tabs[2]:
        st.write("This tab contains actionable **Insights**.")
        st.write("Summarize key findings or predictions here.")
