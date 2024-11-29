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

        /* Form Container */
        .form-container {
            padding: 20px 50px;
            font-family: 'Arial', sans-serif;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px; /* Reduced margin */
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

# Consistent banner
st.markdown('<div class="hero-title">Sign Up to Learn More</div>', unsafe_allow_html=True)

# Form Section
st.markdown('<div class="form-container">', unsafe_allow_html=True)
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
