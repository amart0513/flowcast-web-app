import streamlit as st

st.title("Streamlit App with Embedded Dash")

# Embed Dash app (running on localhost:8050)
st.markdown(
    """
    <iframe src="http://127.0.0.1:8050" width="100%" height="800" frameborder="0"></iframe>
    """,
    unsafe_allow_html=True
)
