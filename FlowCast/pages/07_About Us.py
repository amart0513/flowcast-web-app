import streamlit as st

# Define images
IMAGE_JESUS = "media/JesusPic.jpg"
IMAGE_ANGIE = "media/AngiePic.jpg"
IMAGE_STEVEN = "media/StevenPic.jpg"
IMAGE_CHRIS = "media/ChrisPic.jpg"

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
        }

        /* Subheader Styling */
        .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73;
            margin-bottom: 20px;
            text-align: center;
        }

        /* Team Card Styling */
        .team-card {
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        .team-card img {
            border-radius: 50%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 150px;
            height: 150px;
        }
        .team-card h3 {
            font-size: 1.2rem;
            font-weight: bold;
            color: #005f73;
            margin-top: 10px;
        }
        .team-card p {
            font-size: 0.9rem;
            color: #333;
            margin-top: 5px;
        }

        /* Divider */
        .divider {
            border-top: 2px solid #005f73;
            margin: 20px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to display centered image with caption
def centered_image(image_path, caption, width=200):
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
            <img src="{image_path}" alt="{caption}" style="border-radius: 50%; width: {width}px; height: {width}px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <p style="text-align: center; font-size: 0.9rem; color: gray;">{caption}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Banner Title
st.markdown('<div class="hero-title">Meet the FlowCast Team</div>', unsafe_allow_html=True)

# About Us Content in Tabs
st.markdown('<p class="styled-subheader">Learn more about each team member and their contributions to FlowCast.</p>', unsafe_allow_html=True)
tabs = st.tabs(["Jesus Elespuru", "Angie Martinez", "Steven Luque", "Christopher Perez"])

# Jesus Elespuru
with tabs[0]:
    centered_image(IMAGE_JESUS, caption="Jesus Elespuru")
    st.markdown(
        """
        <div class="team-card">
            <h3>Jesus Elespuru</h3>
            <p>Senior, Back-End Developer & Hardware Designer</p>
            <p>Florida International University</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "Jesus contributed to FlowCast as a back-end developer, focusing on the server-side architecture and API integrations. "
        "He also played a key role in hardware design, ensuring that the physical components of the system met the project's "
        "technical specifications and worked seamlessly with the software."
    )

# Angie Martinez
with tabs[1]:
    centered_image(IMAGE_ANGIE, caption="Angie Martinez")
    st.markdown(
        """
        <div class="team-card">
            <h3>Angie Martinez</h3>
            <p>Senior, Full-Stack Developer, Software Designer & Project Manager</p>
            <p>Florida International University</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "Angie served as the full-stack developer for FlowCast, excelling in both front-end and back-end development. She also led the "
        "software design efforts, ensuring the application was robust and user-friendly. As project manager, Angie coordinated team efforts "
        "and ensured deadlines were met while maintaining the project's overall vision."
    )

# Steven Luque
with tabs[2]:
    centered_image(IMAGE_STEVEN, caption="Steven Luque")
    st.markdown(
        """
        <div class="team-card">
            <h3>Steven Luque</h3>
            <p>Senior, Hardware Designer & Wiring Integration Specialist</p>
            <p>Florida International University</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "Steven's expertise in hardware design was instrumental to FlowCast's success. He focused on integrating wiring components and ensuring "
        "the hardware setup functioned effectively in real-world conditions. His contributions ensured the smooth operation of all hardware components."
    )

# Christopher Perez
with tabs[3]:
    centered_image(IMAGE_CHRIS, caption="Christopher Perez")
    st.markdown(
        """
        <div class="team-card">
            <h3>Christopher Perez</h3>
            <p>Senior, Mathematics & Circuit Analysis</p>
            <p>Florida International University</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "Christopher applied his strong background in mathematics and circuit analysis to optimize the electronic systems of FlowCast. "
        "His work involved ensuring the accuracy of sensor data and the efficiency of circuit designs, which formed the backbone of the system's data collection processes."
    )

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Closing Note
st.write(
    "The FlowCast team collaborated on every aspect of the project, from field data collection to designing and deploying "
    "the application. Their shared expertise has brought FlowCast to life, enabling real-time water quality insights for "
    "environmental preservation."
)
