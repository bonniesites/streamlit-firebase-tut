import streamlit as st

st.set_page_config(
       page_title='My Reddit App',
       layout='wide',
       page_icon=':female-technologist:',
       initial_sidebar_state='expanded',
       menu_items={
              'Get Help': 'https://my-reddit.streamlit.app/',
              'Report a bug': 'https://my-reddit.streamlit.app/',
              'About': '# This is a header. '
       }
)

custom_format = '''
       <style>
       body {
       background-image: url('https://images.unsplash.com/photo-1542281286-9e0a16bb7366');
       background-size: cover;
       }
       footer {visibility: hidden;}
       .css-1wbqy5l e17vllj40  {visibility: hidden; }
       </style>
       '''
st.markdown(custom_format, unsafe_allow_html=True)
