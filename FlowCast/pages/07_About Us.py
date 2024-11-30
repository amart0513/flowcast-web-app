import streamlit as st

IMAGE_JESUS = "media/JesusPic.jpg"
IMAGE_ANGIE = "media/AngiePic.jpg"

st.set_page_config(page_title="FlowCast", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")


def load_media(column, file_path, caption):
    with column:
        if file_path.endswith(".jpeg") or file_path.endswith(".PNG") or file_path.endswith(".jpg"):
            column.image(file_path, caption=caption, width=200)
        elif file_path.endswith(".mp4"):
            column.video(file_path)
        elif file_path.endswith(".mp3"):
            column.audio(file_path)


st.title("About Us")
st.subheader("Get to Know the Team!")
st.divider()
col1, col2, col3, col4 = st.columns(4)
load_media(col2, IMAGE_JESUS, "Jesus Elespuru, Senior, Front-End Developer, Data-Collection, Florida International "
                              "University")
load_media(col3, IMAGE_ANGIE,
           "Angie Martinez, Senior, Back-End Developer, Data-Collection, Florida International University")
st.divider()
col5, col6, col7 = st.columns([1, 1, 1])
