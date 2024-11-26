import streamlit as st

IMAGE_FIU_BANNER = "media/FIU_Banner.png"

st.set_page_config(page_title="FlowCast", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")

st.title("FlowCast: Real-Time Water Monitoring and Prediction")
st.subheader("Home")
# Project overview paragraph
st.write("As soon-to-graduate computer science students participating in ShellHacks 2024,\
 we were driven by a shared commitment to addressing one of the world’s most critical challenges—access\
  to clean and safe water. The motivation behind developing a Streamlit website that leverages machine learning\
   for water quality forecasting stems from this urgency. Clean water is fundamental not only to public health,\
    but also to environmental preservation and sustainable economic development. However, many regions, both in \
    developed and developing countries, struggle with monitoring and managing water resources effectively.")

st.write("Our project was designed to bridge this gap by creating a tool that empowers communities, local governments,\
 and environmental organizations with a real-time, user-friendly platform for forecasting water quality. With machine\
  learning at its core, the website processes historical and real-time data to make accurate predictions about water safety,\
   offering insights that can help prevent waterborne diseases, reduce pollution, and support long-term environmental sustainability efforts.")

st.write("By building this solution, we hope to contribute to raising awareness about global water challenges while showcasing the potential\
 of modern technology in addressing them. Additionally, our project serves as a testament to the power of cross-disciplinary collaboration,\
  where computer science, data analytics, and environmental science come together to make a tangible impact.")

st.divider()
st.subheader("Impact on Society")
st.write("We are committed to leveraging technology to solve real-world problems, and water quality monitoring represents\
 a critical intersection between environmental sustainability and public health. By building a system that can not only predict\
  potential contamination but also detect subtle changes in water quality, our goal is to empower communities, researchers, and policymakers\
   with actionable insights. ")

st.write("Our machine learning-driven platform serves as an accessible tool designed for a broad audience. Communities can use\
 it to monitor their local water sources and receive early warnings about potential hazards, such as bacterial contamination or\
  harmful algal blooms. Researchers can benefit from real-time data and predictive analytics to better understand water quality\
   trends over time. Policymakers, armed with this information, can make informed decisions to protect public health, ensure regulatory\
    compliance, and take timely, proactive measures to safeguard water supplies.")
st.write("Ultimately, our team aims to create a system that bridges the gap between complex environmental data and everyday users, making\
 it easier for people to engage with water quality issues and take preventive action to ensure safe, clean water for all.")

# Data collection and analysis paragraph
st.divider()
st.subheader("Machine Learning and Innovation")
st.write("This hackathon provides the ideal platform to experiment with machine learning models in a real-world, impactful\
 context. By working with water quality data—such as pH levels, dissolved oxygen, contaminants, temperature, and more—we are\
  able to apply our technical knowledge to address a pressing global issue. Through careful analysis of both historical data and\
   real-time inputs, we aim to build a model that predicts future water quality trends with high accuracy. This predictive capability\
    could help in identifying potential hazards early on, such as contamination or the onset of harmful algal blooms.")

st.write("Additionally, this project gives us the chance to bridge theory with practice by applying what we've learned\
 in data science and machine learning to a problem that has profound implications for public health, environmental sustainability,\
  and community well-being. By the end of the hackathon, our goal is to have developed a working system that not only demonstrates\
   our technical expertise but also contributes to a socially relevant cause—ensuring access to clean water through better monitoring and forecasting.")

st.divider()
st.subheader("Accessibility and Usability")
st.write("Streamlit is a powerful yet easy-to-use framework that enables rapid development of interactive web applications,\
 making it an ideal choice for our water quality forecasting tool. Its simplicity allows us to focus on building an intuitive\
  user interface while handling complex data and machine learning models on the backend. By using Streamlit, we can present intricate\
   water quality data—such as pH levels, contaminant concentrations, and predictive trends—in a clean, user-friendly format that’s easily\
    accessible to a broad audience.")

st.write("Our goal is to make this tool valuable not only for government agencies and environmental researchers but also for local"
         "\ communities and individuals who want to monitor their water supply. Streamlit’s interactive features will allow users to"
         "\ explore real-time data and forecasts in a way that’s both visually engaging and informative. Whether it's policymakers making"
         "\ data-driven decisions, researchers tracking environmental changes, or individuals concerned about the quality of their water,"
         "\ our platform is designed to empower users with the information they need to take proactive steps in safeguarding their water resources.")

# Footer
st.divider()
col5, col6, col7 = st.columns([1, 1, 1])
with col6:
    st.image(IMAGE_FIU_BANNER, width=200)

