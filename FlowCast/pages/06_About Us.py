import streamlit as st
import os

# Define image paths
IMAGE_JESUS = "media/JesusPic.jpg"
IMAGE_ANGIE = "media/AngiePic.jpg"
IMAGE_STEVEN = "media/StevenPic.jpg"
IMAGE_CHRIS = "media/ChrisPic.jpg"

# Helper function to verify image paths
def verify_image_path(path):
    if os.path.exists(path):
        return path
    else:
        st.error(f"Image file not found: {path}")
        return None

# Verify all image paths
IMAGE_JESUS = verify_image_path(IMAGE_JESUS)
IMAGE_ANGIE = verify_image_path(IMAGE_ANGIE)
IMAGE_STEVEN = verify_image_path(IMAGE_STEVEN)
IMAGE_CHRIS = verify_image_path(IMAGE_CHRIS)

# Page configuration
st.set_page_config(
    page_title="FlowCast: About Us",
    layout="wide",
    page_icon="🌊",
    initial_sidebar_state="expanded",
)

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
            font-family: "Consolas", monospace;
        }

        /* Section Title Styling */
        .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73;
            margin-bottom: 15px;
            font-family: "Consolas", monospace;
        }

        /* Container Styling */
        .info-container {
            background-color: #f7f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            font-family: "Consolas", monospace;
        }

        /* Divider Styling */
        .divider {
            border-top: 2px solid #005f73;
            margin: 20px 0;
        }

        /* Image Styling */
        .centered-image img {
            border-radius: 50%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 200px;
            height: 200px;
            corner-radius: 50px;
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
            font-family: "Consolas", monospace;
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
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0a9396; /* Match the lighter blue from the banner gradient */
            color: white;
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
            font-family: "Consolas", monospace;
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

# Banner Title
st.markdown('<div class="hero-title">Meet the FlowCast Team</div>', unsafe_allow_html=True)

# Tabs for each team member
tabs = st.tabs(["Jesus Elespuru", "Angie Martinez", "Steven Luque", "Christopher Perez"])

# Jesus Elespuru
with tabs[0]:
    col1, col2 = st.columns([1, 2])
    with col1:
        if IMAGE_JESUS:
            st.image(IMAGE_JESUS, use_container_width=True)
    with col2:
        st.markdown('<p class="styled-subheader">Jesus Elespuru</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Role:</strong> Product Owner, Back-End Developer & Hardware Designer<br>
                <strong>University:</strong> Florida International University<br>
                <strong>College:</strong> Knight Foundation School of Computing and Information Sciences<br>
                <strong>Major:</strong> Computer Science, B.S.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Experience:</strong><br>
                Jesus brings years of experience in back-end development and hardware design, specializing in systems integration 
                and performance optimization. With a solid understanding of APIs, databases, and IoT devices, he excels in creating 
                robust, scalable solutions.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Contributions:</strong><br>
                - Developed and optimized the server-side architecture for real-time data processing.<br>
                - Designed hardware components to ensure reliable integration with software systems.<br>
                - Built custom API solutions for seamless data communication.<br>
                - Collaborated with team members to test and debug the hardware for varied conditions.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Angie Martinez
with tabs[1]:
    col1, col2 = st.columns([1, 2])
    with col1:
        if IMAGE_ANGIE:
            st.image(IMAGE_ANGIE, use_container_width=True)
    with col2:
        st.markdown('<p class="styled-subheader">Angie Martinez</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Role:</strong> Team Lead, Full-Stack Developer, Software Designer & Project Manager<br>
                <strong>University:</strong> Florida International University<br>
                <strong>College:</strong> Knight Foundation School of Computing and Information Sciences<br>
                <strong>Major:</strong> Computer Science, B.S.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Experience:</strong><br>
                Angie has extensive experience in software design and full-stack development. She has a track record of delivering 
                user-friendly applications with optimized back-end systems. Her leadership experience spans multiple collaborative projects.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Contributions:</strong><br>
                - Designed FlowCast's user-friendly interface.<br>
                - Created back-end systems for efficient data processing.<br>
                - Led the team as project manager.<br>
                - Conducted extensive testing to ensure application stability.<br>
                - Championed FlowCast's vision and aligned team efforts.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Repeat similar structure for Steven and Christopher
# Steven Luque
with tabs[2]:
    col1, col2 = st.columns([1, 2])
    with col1:
        if IMAGE_STEVEN:
            st.image(IMAGE_STEVEN, use_container_width=True)
    with col2:
        st.markdown('<p class="styled-subheader">Steven Luque</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Role:</strong> Hardware Designer & Wiring Integration Specialist<br>
                <strong>University:</strong> Florida International University<br>
                <strong>College:</strong> Knight Foundation School of Computing and Information Sciences<br>
                <strong>Major:</strong> Computer Science, B.S.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Experience:</strong><br>
                Steven is an experienced hardware designer with expertise in IoT devices and embedded systems. His hands-on approach 
                has enabled him to troubleshoot and refine designs for optimal performance in demanding environments. He specializes 
                in wiring integration and ensuring hardware operates seamlessly with other system components.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Contributions:</strong><br>
                - Designed and implemented the wiring system that connected FlowCast's sensors and devices.<br>
                - Conducted rigorous testing of hardware configurations to ensure durability and reliability.<br>
                - Researched and sourced cost-effective hardware solutions that met project specifications.<br>
                - Enhanced system efficiency by fine-tuning wiring configurations.<br>
                - Ensured hardware outputs aligned seamlessly with software requirements.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Christopher Perez
with tabs[3]:
    col1, col2 = st.columns([1, 2])
    with col1:
        if IMAGE_CHRIS:
            st.image(IMAGE_CHRIS, use_container_width=True)
    with col2:
        st.markdown('<p class="styled-subheader">Christopher Perez</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Role:</strong> Mathematics & Circuit Analysis<br>
                <strong>University:</strong> Florida International University<br>
                <strong>College:</strong> Knight Foundation School of Computing and Information Sciences<br>
                <strong>Major:</strong> Computer Science, B.S.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Experience:</strong><br>
                Christopher has a strong background in mathematics and circuit analysis. His expertise lies in optimizing electrical 
                systems for energy efficiency and data accuracy. His analytical mindset ensures precision in data collection and system performance.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-container">
                <strong>Contributions:</strong><br>
                - Analyzed and optimized FlowCast's circuit designs for accurate sensor readings.<br>
                - Applied advanced mathematical models to validate data reliability.<br>
                - Designed energy-efficient circuit solutions to extend hardware life.<br>
                - Debugged and refined sensors to ensure accuracy under varying environmental conditions.<br>
                - Collaborated with hardware and software teams to integrate sensor outputs into analytics.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Closing Note
st.write("The FlowCast team collaborated on every aspect of the project, from field data collection to designing and "
         "deploying the application. Their shared expertise has brought FlowCast to life, enabling real-time water "
         "quality insights for environmental preservation.")

st.write("Through extensive teamwork, the group overcame numerous technical challenges, including integrating "
         "cutting-edge sensor technology with robust machine learning models. By combining diverse skill sets in "
         "software development, hardware design, mathematics, and project management, they created a seamless system "
         "that bridges the gap between raw environmental data and actionable insights. This synergy underscores the "
         "value of interdisciplinary collaboration in tackling real-world issues like water quality monitoring.")

st.write("FlowCast’s innovative approach has the potential to make a lasting impact on marine ecosystems and coastal "
         "communities. By providing accurate, real-time data, the platform empowers researchers, policymakers, "
         "and local organizations to make informed decisions for sustainable resource management. Beyond its "
         "technological achievements, FlowCast stands as a testament to what can be accomplished when passionate "
         "individuals work together toward a shared vision for environmental preservation.")
