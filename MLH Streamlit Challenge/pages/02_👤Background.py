import streamlit as st

IMAGE1 = "media/boat1.jpg"
IMAGE2 = "media/boat2.jpg"
IMAGE_FIU_BANNER = "media/FIU_Banner.png"

st.set_page_config(page_title="FlowCast", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")


def render_background():
    st.title("Background")
    st.subheader("About our Project")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Our project centered on the real-time analysis of water quality using advanced machine learning techniques\
        , specifically tailored for the unique environmental conditions of Biscayne Bay and Haulover Beach. The core of our approach\
         was the seamless integration of field data, collected directly from these two coastal locations, into our machine learning\
          models. This data included key water quality parameters such as pH levels, temperature, salinity, turbidity, and the presence\
           of harmful pollutants or bacteria.")

        st.write("By focusing on location-specific datasets, we were able to train our machine learning algorithms on highly relevant\
         and accurate information, which significantly improved the performance of our predictive models. The real-time aspect of the\
          analysis meant that the system could continuously update its predictions as new data became available, allowing it to forecast\
           future water quality conditions with remarkable precision.")

        st.write("In practice, this solution could provide early warnings about potential water quality issues, such as harmful\
         algal blooms or bacterial contamination, that could affect both marine life and human health. Additionally, the insights\
          from our models have the potential to inform policymakers and environmental agencies, aiding in the timely implementation\
           of conservation measures or advisories for recreational beachgoers. Overall, this project highlights the power of combining\
            machine learning with environmental data to address real-world challenges in water quality monitoring and preservation.")
    with col2:
        st.image(IMAGE1, use_column_width=True)

    # Subheader and paragraph for additional information
    st.divider()
    st.subheader("Data Collection Process")
    col3, col4 = st.columns(2)

    with col3:
        # Data retrieval and training process
        st.write("Throughout our expeditions, we utilized cutting-edge sensors and automated sampling systems to gather \
                   a comprehensive dataset on key water quality parameters, including temperature, pH, dissolved oxygen, and nutrient concentrations. \
                   Each measurement was paired with precise GPS coordinates, ensuring that the data collected was both geospatially and \
                   temporally accurate. This granular dataset laid the foundation for our machine learning model, enabling us to analyze \
                   water quality patterns with fine detail and precision.")
        # Explanation of data preparation for model training
        st.write("To prepare the data for machine learning training, we performed a thorough cleaning and preprocessing step, removing \
                   any inconsistencies and outliers to ensure the integrity of the dataset. The processed data was then divided into training \
                   and testing sets, with the training set used to fit our machine learning model. We employed techniques like feature scaling, \
                   normalization, and cross-validation to optimize the model's performance and reduce potential biases.")
        # Integration of real-time data and visual assets
        st.write("Real-time data from NOAA’s API was also integrated into the dataset, providing up-to-date environmental variables \
                   for continuous model refinement. Alongside the raw data, we documented geographical features, marine life, and human activities \
                   in the study areas through photographs and videos. These visuals not only enriched the understanding of water quality trends \
                   but also served as powerful tools for community engagement and awareness regarding conservation efforts.")
    with col4:
        st.image(IMAGE2, use_column_width=True)

    st.divider()
    # col5, col6, col7 = st.columns([1, 1, 1])


render_background()
