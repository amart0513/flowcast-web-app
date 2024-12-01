import streamlit as st

IMAGE1 = "media/boat1.jpg"
IMAGE2 = "media/boat2.jpg"

st.set_page_config(page_title="FlowCast", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* General Styles */

        .hero-title {
            font-size: 2.8rem;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(135deg, #005f73, #0a9396);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            font-family: "Consolas", monospace;
        }
        .section-header {
            font-size: 2.5rem;
            text-align: center;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #005f73;
            font-family: "Consolas", monospace;
        }
        .divider {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, #005f73, #0a9396, #005f73);
            margin: 30px 0;
        }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            font-family: "Consolas", monospace;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .card img {
            border-radius: 10px;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }
        .card img:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .rounded-image {
            border-radius: 10px;
        }
        .back-to-top {
            text-align: center;
            margin-top: 30px;
        }
        .back-to-top a {
            text-decoration: none;
            font-size: 1.2rem;
            color: #0a9396;
            font-weight: bold;
        }
        .back-to-top a:hover {
            color: #005f73;
            text-decoration: underline;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Custom CSS for Styling and Sidebar
st.markdown(
    """
    <style>
        /* General Styles */
        body {
            margin: 0;
            padding: 0;
        }
        .section-header {
            font-size: 2.5rem;
            text-align: center;
            margin-top: 50px;
            margin-bottom: 20px;
            color: #005f73;
            font-family: "Consolas", monospace;
        }
        .divider {
            border-top: 1px solid #ccc;
            margin: 30px 0;
        }
        /* Hero Section */
        .hero-section {
            position: relative;
            background: linear-gradient(135deg, rgba(0, 95, 115, 0.9), rgba(10, 147, 150, 0.9)), url('media/FIU_Banner.png');
            background-size: cover;
            background-position: center;
            color: white;
            text-align: center;
            padding: 100px 20px;
            border-radius: 10px;
            animation: fadeIn 1.5s ease-in-out;
            margin-bottom: 0; /* Removes the light gray gap */
        }
        .hero-title {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 15px;
            color: white;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            margin-bottom: 40px;
        }
        .button-container a {
            text-decoration: none;
        }
        .button-container button {
            margin: 0 10px;
            padding: 12px 30px;
            font-size: 1rem;
            color: white;
            background-color: #0a9396;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.3s ease-in-out, background-color 0.3s;
        }
        .button-container button:hover {
            background-color: white;
            color: #005f73;
            transform: scale(1.05);
        }
        /* Cards */
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease-in-out, box-shadow 0.3s;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }
        .card img {
            border-radius: 15px;
            width: 100%;
        }
        .card p {
            margin-top: 10px;
        }
        /* Animation */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0a9396; /* Match the lighter blue from the banner gradient */
            color: #005f73;
            padding: 20px;
            font-family: "Consolas", monospace;
        }

        [data-testid="stSidebar"] h3 {
            color: white;
            font-weight: bold;
            margin-bottom: 20px;
            font-family: "Consolas", monospace;
        }

        [data-testid="stSidebar"] label {
            font-size: 1rem;
            color: white;
        }

        [data-testid="stSidebar"] button {
            background-color: #005f73;
            color: white;
            font-size: 1rem;
            border-radius: 8px;
            padding: 10px 15px;
            margin: 10px 0;
            border: none;
            cursor: pointer;
            transition: transform 0.2s, background-color 0.3s;
        }

        [data-testid="stSidebar"] button:hover {
            background-color: #ffffff;
            color: #005f73;
            transform: scale(1.05);
        }

        [data-testid="stSidebar"] .stSelectbox {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 8px;
            padding: 5px;
            margin: 10px 0;
            font-family: "Consolas", monospace;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_background():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Styled Title Section
    st.markdown('<div class="hero-title">Background</div>', unsafe_allow_html=True)

    # About the Project Section
    st.markdown('<h2 class="section-header">About Our Project</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <p>
                Our project centered on the real-time analysis of water quality using advanced machine learning techniques,
                specifically tailored for the unique environmental conditions of Biscayne Bay and Haulover Beach. The core of our approach
                was the seamless integration of field data, collected directly from these two coastal locations, into our machine learning
                models. This data included key water quality parameters such as pH levels, temperature, salinity, turbidity, and the presence
                of harmful pollutants or bacteria.
                </p>
                <p>
                By focusing on location-specific datasets, we were able to train our machine learning algorithms on highly relevant
                and accurate information, which significantly improved the performance of our predictive models. The real-time aspect of the
                analysis meant that the system could continuously update its predictions as new data became available, allowing it to forecast
                future water quality conditions with remarkable precision.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.image(IMAGE1, caption="The Heron collecting water quality data.", use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Data Collection Process Section
    st.markdown('<h2 class="section-header">Data Collection Process</h2>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div class="card">
                <p>
                Throughout our expeditions, we utilized cutting-edge sensors and automated sampling systems to gather 
                a comprehensive dataset on key water quality parameters, including temperature, pH, dissolved oxygen, and nutrient concentrations.
                Each measurement was paired with precise GPS coordinates, ensuring that the data collected was both geospatially and
                temporally accurate. This granular dataset laid the foundation for our machine learning model, enabling us to analyze
                water quality patterns with fine detail and precision.
                </p>
                <p>
                To prepare the data for machine learning training, we performed a thorough cleaning and preprocessing step, removing
                any inconsistencies and outliers to ensure the integrity of the dataset. The processed data was then divided into training
                and testing sets, with the training set used to fit our machine learning model. We employed techniques like feature scaling,
                normalization, and cross-validation to optimize the model's performance and reduce potential biases.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.image(IMAGE2, caption="Our team preparing for data collection in Biscayne Bay.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Insights Section
    st.markdown('<h2 class="section-header">Real-Time Insights</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
            <p>
            Real-time data from NOAA’s API was also integrated into the dataset, providing up-to-date environmental variables
            for continuous model refinement. Alongside the raw data, we documented geographical features, marine life, and human activities
            in the study areas through photographs and videos. These visuals not only enriched the understanding of water quality trends
            but also served as powerful tools for community engagement and awareness regarding conservation efforts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


render_background()
