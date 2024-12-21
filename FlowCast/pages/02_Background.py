import streamlit as st

IMAGE1 = "media/boat1.jpg"
IMAGE2 = "media/boat2.jpg"
IMAGE3 = "media/boat3.jpeg"
IMAGE4 = "media/team-pic.jpeg"
IMAGE5 = "media/boat4.jpeg"
IMAGE6 = "media/team-pic2.jpeg"
IMAGE7 = "media/jesus-pic.jpeg"

st.set_page_config(page_title="Project Background", layout="wide",
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
            animation: fadeIn 1.5s ease-in-out;
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
    st.markdown(
        "<h2 class=\"section-header\">Enhancing Environmental Monitoring with Python</h2>",
        unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # markdown 1
        st.markdown(
            """
            <div class="card">
                <p>
                Our project leverages <b>advanced machine learning techniques</b> to monitor and predict water quality in real-time, 
                with a focus on <b>Biscayne Bay</b> and <b>Haulover Beach</b>. By tailoring models to these unique environments, 
                we developed a robust system that provides actionable insights into aquatic conditions, benefiting both marine ecosystems 
                and public health.
                </p>
                <ul>
                    <li>
                        <b>Location-Specific Dataset Integration:</b>  
                        - Curated datasets uniquely relevant to Biscayne Bay and Haulover Beach, accounting for local environmental factors.  
                        - This approach significantly improved predictive accuracy compared to generic models.
                    </li>
                    <li>
                        <b>Machine Learning Models for Forecasting:</b>  
                        - Trained models capable of detecting trends and anomalies in water quality metrics using Python libraries like 
                          Scikit-learn and TensorFlow.  
                        - Predictive capabilities allow stakeholders to respond proactively to potential threats such as <i>fish kills</i> or 
                          <i>pollution spikes</i>.
                    </li>
                    <li>
                        <b>Real-Time Data Integration:</b>  
                        - Fetches live environmental data from APIs like NOAA, ensuring up-to-date analysis.  
                        - Real-time updates visualized through interactive dashboards built with <b>Streamlit</b>.
                    </li>
                </ul>
                <p>
                By automating the data collection from the EXO2 sonde and providing a web interface for viewing both real-time and historical 
                data, the system reduces manual effort, improves data accuracy, and enhances accessibility for researchers, technicians, or 
                anyone involved in water quality monitoring. The project’s goal is to create a scalable solution that can be adapted for various 
                environmental and scientific applications, promoting more efficient and informed decision-making in water quality management.
                This Python-driven initiative not only underscores the potential of technology in environmental protection but also sets 
                a precedent for how location-specific data can redefine the scope and efficacy of predictive analytics.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # markdown 2
        st.markdown(
            """
            <div class="card">
                <p>
                Our project leverages <b>advanced machine learning techniques</b> to monitor and predict water quality in real-time, 
                with a focus on <b>Biscayne Bay</b> and <b>Haulover Beach</b>. By tailoring models to these unique environments, 
                we developed a robust system that provides actionable insights into aquatic conditions, benefiting both marine ecosystems 
                and public health.
                </p>
                <ul>
                    <li>
                        <b>Location-Specific Dataset Integration:</b>  
                        - Curated datasets uniquely relevant to Biscayne Bay and Haulover Beach, accounting for local environmental factors.  
                        - This approach significantly improved predictive accuracy compared to generic models.
                    </li>
                    <li>
                        <b>Machine Learning Models for Forecasting:</b>  
                        - Trained models capable of detecting trends and anomalies in water quality metrics using Python libraries like 
                          Scikit-learn and TensorFlow.  
                        - Predictive capabilities allow stakeholders to respond proactively to potential threats such as <i>fish kills</i> or 
                          <i>pollution spikes</i>.
                    </li>
                    <li>
                        <b>Real-Time Data Integration:</b>  
                        - Fetches live environmental data from APIs like NOAA, ensuring up-to-date analysis.  
                        - Real-time updates visualized through interactive dashboards built with <b>Streamlit</b>.
                    </li>
                </ul>
                <p>
                By automating the data collection from the EXO2 sonde and providing a web interface for viewing both real-time and historical 
                data, the system reduces manual effort, improves data accuracy, and enhances accessibility for researchers, technicians, or 
                anyone involved in water quality monitoring. The project’s goal is to create a scalable solution that can be adapted for various 
                environmental and scientific applications, promoting more efficient and informed decision-making in water quality management.
                This Python-driven initiative not only underscores the potential of technology in environmental protection but also sets 
                a precedent for how location-specific data can redefine the scope and efficacy of predictive analytics.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # markdown 3
        st.markdown(
            """
            <div class="card">
                <p>
                Our project leverages <b>advanced machine learning techniques</b> to monitor and predict water quality in real-time, 
                with a focus on <b>Biscayne Bay</b> and <b>Haulover Beach</b>. By tailoring models to these unique environments, 
                we developed a robust system that provides actionable insights into aquatic conditions, benefiting both marine ecosystems 
                and public health.
                </p>
                <ul>
                    <li>
                        <b>Location-Specific Dataset Integration:</b>  
                        - Curated datasets uniquely relevant to Biscayne Bay and Haulover Beach, accounting for local environmental factors.  
                        - This approach significantly improved predictive accuracy compared to generic models.
                    </li>
                    <li>
                        <b>Machine Learning Models for Forecasting:</b>  
                        - Trained models capable of detecting trends and anomalies in water quality metrics using Python libraries like 
                          Scikit-learn and TensorFlow.  
                        - Predictive capabilities allow stakeholders to respond proactively to potential threats such as <i>fish kills</i> or 
                          <i>pollution spikes</i>.
                    </li>
                    <li>
                        <b>Real-Time Data Integration:</b>  
                        - Fetches live environmental data from APIs like NOAA, ensuring up-to-date analysis.  
                        - Real-time updates visualized through interactive dashboards built with <b>Streamlit</b>.
                    </li>
                </ul>
                <p>
                By automating the data collection from the EXO2 sonde and providing a web interface for viewing both real-time and historical 
                data, the system reduces manual effort, improves data accuracy, and enhances accessibility for researchers, technicians, or 
                anyone involved in water quality monitoring. The project’s goal is to create a scalable solution that can be adapted for various 
                environmental and scientific applications, promoting more efficient and informed decision-making in water quality management.
                This Python-driven initiative not only underscores the potential of technology in environmental protection but also sets 
                a precedent for how location-specific data can redefine the scope and efficacy of predictive analytics.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:
        st.image(IMAGE3, caption="The Heron collecting data nearby Haulover Beach, FL.", use_container_width=True)
        st.image(IMAGE5, caption="Our boat completely prepared for the upcoming mission on October 25, 2024 at the "
                                 "Biscayne Bay Campus in Miami, FL.", use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Data Collection Process Section
    st.markdown('<h2 class="section-header">Data Collection Process</h2>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div class="card">
                <p>
                The data collection process for our project was meticulously designed to ensure precision, reliability, and relevance, laying a strong foundation 
                for real-time water quality analysis and machine learning applications. By combining field measurements, external data sources, and advanced 
                processing techniques, we achieved a comprehensive and scalable system.
                </p>
                <ul>
                    <li>
                        <b>Integration with High-Precision Sensors:</b>  
                        - Employed the EXO2 sonde to measure critical parameters such as pH, temperature, salinity, turbidity, dissolved oxygen, and chlorophyll levels.  
                        - Configured automated data logging intervals to capture continuous environmental fluctuations.  
                        - Enhanced sensor performance with calibration routines to reduce measurement errors.
                    </li>
                    <li>
                        <b>Real-Time API Data Streams:</b>  
                        - Sourced live environmental data from NOAA and other reliable platforms to supplement physical measurements.  
                        - Utilized APIs to gather additional metadata, such as weather conditions, tidal information, and historical records, enriching the dataset.  
                        - Ensured synchronization between external and on-site data streams for seamless integration.
                    </li>
                    <li>
                        <b>Rigorous Data Validation and Processing:</b>  
                        - Implemented Python-based pipelines with libraries like Pandas and NumPy to clean, filter, and validate incoming data.  
                        - Addressed missing values through imputation techniques and removed outliers using statistical thresholds.  
                        - Conducted exploratory data analysis (EDA) to identify trends and anomalies in the collected data.
                    </li>
                    <li>
                        <b>Scalability for Future Expansion:</b>  
                        - Designed the system to accommodate additional sensors and new data streams as project requirements evolve.  
                        - Ensured modularity in the collection process, enabling easy updates to hardware and software components.  
                        - Established documentation for replicability, facilitating adoption by other environmental monitoring initiatives.
                    </li>
                </ul>
                <p>
                Through this multi-faceted approach, our data collection process not only guarantees high-quality input for machine learning models but also 
                positions the project as a scalable and impactful solution for water quality monitoring and environmental conservation.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.image(IMAGE4, caption="Our team preparing for data collection in Biscayne Bay.", use_container_width=True)
        st.image(IMAGE6, caption="Reassembling the ASV for second deployment onto the bay.", use_container_width=True)
        st.image(IMAGE7, caption="Preparing the ASV for third deployment onto the bay.", use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Insights Section
    st.markdown('<h2 class="section-header">Real-Time Insights</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
            <p>
            The integration of <b>real-time data streams</b> from NOAA’s API allowed us to incorporate up-to-date environmental variables, 
            such as water temperature, salinity, tidal levels, and weather conditions, directly into our predictive models. This seamless 
            integration ensured that our system remained dynamic, continuously adapting to the most current environmental changes.
            </p>
            <ul>
                <li>
                    <b>Dynamic Model Refinement:</b>  
                    - Real-time data empowered our machine learning models to evolve continuously by retraining on the latest environmental inputs.  
                    - This adaptability significantly enhanced predictive accuracy, particularly during rapidly changing conditions.
                </li>
                <li>
                    <b>Visual Documentation and Analysis:</b>  
                    - Captured photographs and videos of study areas to document geographical features, marine life behaviors, and human activities.  
                    - These visuals provided context for data-driven insights and highlighted the impact of environmental changes on local ecosystems.
                </li>
                <li>
                    <b>Community Engagement and Awareness:</b>  
                    - Leveraged visual content to create compelling narratives for public outreach, fostering awareness about water quality issues.  
                    - Designed interactive dashboards to make real-time insights accessible to stakeholders, from environmental scientists to local communities.
                </li>
                <li>
                    <b>Actionable Insights for Conservation:</b>  
                    - Delivered timely forecasts of water quality metrics, enabling proactive measures to mitigate risks such as pollution spikes or marine habitat disruptions.  
                    - Provided data-driven recommendations for policy makers and conservationists, enhancing resource management efforts.
                </li>
            </ul>
            <p>
            This combination of data, visuals, and community-focused design ensures that real-time insights are not only scientifically robust but also 
            accessible and impactful, fostering a deeper connection between technology and environmental stewardship.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


render_background()
