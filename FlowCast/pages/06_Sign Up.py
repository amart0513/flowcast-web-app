import streamlit as st

MAJORS = [
    "",  # Placeholder for an empty selection
    "Accounting",
    "Aerospace Engineering",
    "Agricultural Science",
    "Anthropology",
    "Architecture",
    "Art History",
    "Biochemistry",
    "Biomedical Engineering",
    "Chemical Engineering",
    "Civil Engineering",
    "Computer Science",
    "Criminal Justice",
    "Cybersecurity",
    "Dentistry",
    "Economics",
    "Electrical Engineering",
    "Environmental Science",
    "Film Studies",
    "Finance",
    "Graphic Design",
    "History",
    "Industrial Engineering",
    "International Relations",
    "Journalism",
    "Linguistics",
    "Management",
    "Marketing",
    "Mathematics",
    "Mechanical Engineering",
    "Medicine",
    "Music",
    "Nursing",
    "Nutrition",
    "Pharmacy",
    "Philosophy",
    "Physics",
    "Political Science",
    "Psychology",
    "Public Health",
    "Sociology",
    "Software Engineering",
    "Statistics",
    "Theater",
    "Urban Planning",
    "Veterinary Science",
    "Web Development"
]

st.set_page_config(page_title="FlowCast: Sign Up", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")

# Custom CSS for consistent layout and spacing
st.markdown(
    """
    <style>
        /* Consistent Banner */
        .hero-title {
            font-size: 3rem;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(135deg, #005f73, #0a9396);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 10px; /* Minimized margin */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Divider Style */
        .divider {
            border-top: 2px solid #005f73;
            margin: 10px 0; /* Minimized margin */
        }

        /* Remove Padding from Default Streamlit Elements */
        .stMarkdown {
            padding: 0; /* Remove padding */
            margin: 0; /* Remove margin */
        }

        .stTextInput, .stSelectbox, .stCheckbox, .stButton {
            margin-bottom: 10px; /* Tighten spacing between form elements */
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
        .main-container {
            background-color: blue;
            padding: 20px 50px;
            font-family: 'Arial', sans-serif;
        }
        .section-header {
            font-size: 2.5rem;
            text-align: center;
            margin-top: 50px;
            margin-bottom: 20px;
            color: #005f73;
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
            color: white;
            padding: 20px;
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

# Consistent banner
st.markdown('<div class="hero-title">Sign Up to Learn More</div>', unsafe_allow_html=True)

# Form Section
st.write("Please enter your information below:")

with st.form("Registration", clear_on_submit=True):
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    major = st.selectbox("Major:", options=MAJORS)
    level = st.selectbox("Degree Level:", options=["", "Undergrad", "Masters", "PhD", "Other"])
    subscribe = st.checkbox("Do you want to know about future events?")
    submit = st.form_submit_button("Submit")
    if (name and email and submit and subscribe and level) or (name and email and submit and level):
        st.success(f"{name}, {level} in {major}, is now registered")
    elif submit:
        st.warning(f"{name}, {level} in {major}, is NOT registered")
    else:
        st.info("Please fill out the form.")
st.markdown('</div>', unsafe_allow_html=True)

# Divider for separation
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
