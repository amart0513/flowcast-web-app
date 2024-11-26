import streamlit as st

IMAGE_FIU_BANNER = "media/FIU_Banner.png"

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

st.set_page_config(page_title="FlowCast", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")

st.title('Sign Up to Learn More')
st.write('Please enter your information below:')

with st.form("Registration", clear_on_submit=True):
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    major = st.selectbox("Major:",
                         options=MAJORS)
    level = st.selectbox("Degree Level:", options=["", "Undergrad", "Masters", "PhD", "Other"])
    subscribe = st.checkbox("Do you want to know about future events?")
    submit = st.form_submit_button("Submit")
    if (name and email and submit and subscribe and level) or (name and email and submit and level):
        st.success(f"{name}, {level} in {major}, is now registered")
    elif submit:
        st.warning(f"{name}, {level} in {major}, is NOT registered")
    else:
        st.info("Please Fill out the form")
st.divider()
# col5, col6, col7 = st.columns([1, 1, 1])

