import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde
import requests


# ===============================
# Helper Functions
# ===============================

def safe_float_convert(value, default=0.0):
    try:
        numeric_part = ''.join(c for c in str(value) if c.isdigit() or c in '.-')
        return float(numeric_part) if numeric_part else default
    except (ValueError, TypeError):
        return default


# Fetch active monitoring sites
def get_south_florida_sites():
    base_url = "https://waterservices.usgs.gov/nwis/site/"
    params = {
        "format": "rdb",
        "bBox": "-82.331,25.124,-80.031,26.947",
        "siteStatus": "active",
        "hasDataTypeCd": "qw",
        "siteType": "ST,LK,SP"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        lines = [line for line in response.text.split('\n') if line.strip() and not line.startswith('#')]
        if len(lines) < 2:
            return pd.DataFrame()
        headers = lines[0].strip().split('\t')
        sites = []
        for line in lines[2:]:
            values = line.strip().split('\t')
            if len(values) == len(headers):
                site_dict = dict(zip(headers, values))
                site_entry = {
                    'Site ID': site_dict.get('site_no', '').strip(),
                    'Site Name': site_dict.get('station_nm', '').strip(),
                    'Latitude': safe_float_convert(site_dict.get('dec_lat_va')),
                    'Longitude': safe_float_convert(site_dict.get('dec_long_va')),
                    'State': site_dict.get('state_cd', '').strip(),
                    'County': site_dict.get('county_cd', '').strip()
                }
                if site_entry['Latitude'] != 0 and site_entry['Longitude'] != 0:
                    sites.append(site_entry)
        return pd.DataFrame(sites)
    except requests.exceptions.RequestException:
        return pd.DataFrame()


# Fetch water quality data for a given site and parameter
def get_usgs_water_quality(site_id, start_date, end_date, parameter_codes):
    base_url = "https://waterservices.usgs.gov/nwis/iv/"
    params = {
        "format": "json",
        "sites": site_id,
        "startDT": start_date,
        "endDT": end_date,
        "parameterCd": ",".join(parameter_codes),
        "siteStatus": "all"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        readings = []
        if 'value' in data and 'timeSeries' in data['value']:
            for series in data['value']['timeSeries']:
                parameter_name = series['variable']['variableName']
                for value in series['values'][0]['value']:
                    readings.append({
                        'Timestamp': value['dateTime'],
                        'Parameter': parameter_name,
                        'Value': safe_float_convert(value['value']),
                        'Unit': series['variable']['unit']['unitCode']
                    })
        return pd.DataFrame(readings)
    except requests.exceptions.RequestException:
        return pd.DataFrame()


# ===============================
# Visualization Functions
# ===============================

def create_site_map(sites_df):
    fig = go.Figure(go.Scattermapbox(
        lat=sites_df['Latitude'],
        lon=sites_df['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=10, color='royalblue'),
        text=sites_df['Site Name'],
        hoverinfo='text'
    ))
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center={"lat": sites_df['Latitude'].mean(), "lon": sites_df['Longitude'].mean()},
            zoom=8
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500
    )
    return fig


def create_time_series_chart(data_df, parameter):
    filtered_data = data_df[data_df['Parameter'] == parameter]
    if filtered_data.empty:
        return None
    filtered_data['Timestamp'] = pd.to_datetime(filtered_data['Timestamp'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_data['Timestamp'], y=filtered_data['Value'], mode='lines+markers',
        name=parameter, line=dict(color='blue')
    ))
    fig.update_layout(title=f"Time Series for {parameter}", height=400)
    return fig


def create_summary_statistics(data_df):
    if data_df.empty:
        return None
    summary = data_df.groupby('Parameter')['Value'].describe()
    return summary


# ===============================
# Streamlit Dashboard
# ===============================

def main():
    st.set_page_config(page_title="Enhanced Water Quality Dashboard", layout="wide")
    st.title("Enhanced Water Quality Dashboard")
    st.write("Explore and visualize water quality data from South Florida monitoring sites.")

    with st.spinner("Fetching monitoring sites..."):
        sites_df = get_south_florida_sites()

    if not sites_df.empty:
        st.header("Monitoring Sites")
        st.write("The map below shows all active water quality monitoring sites in South Florida.")
        st.plotly_chart(create_site_map(sites_df), use_container_width=True)

        st.subheader("Site Information")
        st.write("Select a site from the table below to view more details.")
        st.dataframe(sites_df)

        selected_site = st.selectbox("Select a Site ID", sites_df['Site ID'])
        if selected_site:
            st.header("Water Quality Data")
            st.write(f"Showing data for site: {selected_site}")
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
            end_date = st.date_input("End Date", datetime.now())
            params = {
                'Temperature': '00010',
                'Dissolved Oxygen': '00300',
                'pH': '00400',
                'Conductance': '00095'
            }
            selected_params = st.multiselect("Select Parameters", params.keys(), default=list(params.keys()))
            parameter_codes = [params[p] for p in selected_params]

            with st.spinner("Fetching data..."):
                data_df = get_usgs_water_quality(selected_site, start_date.strftime('%Y-%m-%d'),
                                                 end_date.strftime('%Y-%m-%d'), parameter_codes)

            if not data_df.empty:
                st.subheader("Data Summary")
                st.write("Summary statistics for the selected parameters:")
                st.table(create_summary_statistics(data_df))

                st.subheader("Visualizations")
                for param in selected_params:
                    chart = create_time_series_chart(data_df, param)
                    if chart:
                        st.plotly_chart(chart)
            else:
                st.warning("No data available for the selected site and parameters.")


if __name__ == "__main__":
    main()
