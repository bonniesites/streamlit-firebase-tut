import streamlit as st

st.set_page_config(
       page_title="My Reddit App",
       layout="wide",
       page_icon=":female-technologist:",
)

custom_format = """
       <style>
       body {
       background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
       background-size: cover;
       }
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       .css-1wbqy5l e17vllj40  {visibility: hidden; }
       </style>
       """
st.markdown(custom_format, unsafe_allow_html=True)
