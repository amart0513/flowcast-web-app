import streamlit as st

# Define images
IMAGE1 = "media/boat1.jpg"
IMAGE2 = "media/boat2.jpg"

# Page configuration
st.set_page_config(
    page_title="FlowCast",
    layout="wide",
    page_icon="🌊",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://flowcast.example.com/help",
        "Report a bug": "https://flowcast.example.com/report",
        "About": "FlowCast is a real-time water monitoring and prediction app.",
    },
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
            background: linear-gradient(135deg, rgba(0, 95, 115, 0.9), rgba(10, 147, 150, 0.9)), url('');
            background-size: cover;
            background-position: center;
            color: white;
            text-align: center;
            padding: 100px 20px;
            border-radius: 10px;
            animation: fadeIn 1.5s ease-in-out;
            margin-bottom: 0; /* Removes the light gray gap */
            font-family: "Consolas", monospace;
        }
        .hero-title {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 15px;
            color: white;
            font-family: "Consolas", monospace;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            margin-bottom: 40px;
            font-family: "Consolas", monospace;
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
            font-family: "Consolas", monospace;
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
        /* Sidebar Styling--main sidebar */
        [data-testid="stSidebar"] {
            background-color: #0a9396; /* Match the lighter blue from the banner gradient */
            color: black;
            padding: 20px;
            font-family: "Consolas", monospace;
        }

        [data-testid="stSidebar"] h3 {
            color: white;
            font-weight: bold;
            margin-bottom: 20px;
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
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero Section
st.markdown(
    """
    <div class="hero-section">
        <h1 class="hero-title">Welcome to FlowCast</h1>
        <p class="hero-subtitle">
            Real-time water quality insights powered by advanced machine learning.
        </p>
        <div class="button-container">
            <a href="https://protectingfloridatogether.gov/water-quality-status-dashboard">
                <button>Learn More</button>
            </a>
            <a href="https://www.noaa.gov/">
                <button>NOAA Website</button>
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Background Section with Cards
st.markdown('<h2 class="section-header">Our Purpose</h2>', unsafe_allow_html=True)

tab1, tab2 = st.columns([2, 1])
with tab1:
    st.markdown(
        """
        <div class="card">
            <p>
            Our project centered on the real-time analysis of water quality using advanced machine learning techniques, 
            specifically tailored for the unique environmental conditions of Biscayne Bay and Haulover Beach. 
            By focusing on location-specific datasets, we significantly improved predictive model performance, enabling 
            timely forecasts for water quality issues that impact marine life and human health.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.image(IMAGE1, caption="The Heron collecting data from the FIU lake by Parking Garage 6 (PG-6).", use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Data Collection Section with Tabs
st.markdown('<h2 class="section-header">Data Collection Process</h2>', unsafe_allow_html=True)
tab3, tab4 = st.columns([2, 1])

with tab3:
    st.markdown(
        """
        <div class="card">
            <p>
            Using advanced sensors and automated systems, we gathered comprehensive datasets including temperature, pH, 
            dissolved oxygen, and nutrient concentrations. Each measurement was paired with precise GPS coordinates for 
            geospatial accuracy. Our machine learning models underwent rigorous training with techniques like feature scaling 
            and cross-validation to ensure high precision and minimal biases.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab4:
    st.image(IMAGE2, caption="Our boat being prepared for a Biscayne Bay mission to collect data and provide updates "
                             "on the quality of the ocean.", use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
