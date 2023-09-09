import streamlit as st
from mods import base

st.set_page_config(
       page_title='BYU-I PATHWAY STUDY SKILLS',
       layout='centered',
       page_icon='💫',
       initial_sidebar_state='collapsed',
       menu_items={
              'Get Help': 'https://my-reddit.streamlit.app/',
              'Report a bug': 'https://my-reddit.streamlit.app/',
              'About': '# This is a header. '
       }
)

custom_format = '''
       <style>
       #root {
       background-image: url('https://images.unsplash.com/photo-1688453756951-842a78eec6ad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2535&q=80');
       background-size: cover;
       }
       footer {visibility: hidden;}
       .css-1wbqy5l e17vllj40  {visibility: hidden; }
       </style>
       '''
st.markdown(custom_format, unsafe_allow_html=True)

st.title('BYU-I PATHWAY STUDY SKILLS')
st.divider()


urls = {
    'PDF file': 'https://content.byui.edu/file/d901d815-c4ed-4fd0-a731-3762dc38b846/10/BookofMormon_StudySkills.pdf',
    'Substitution': 'http://www.kaltura.com/tiny/ds27r',
    'Setting': 'http://www.kaltura.com/tiny/f6rue',
    'Principles & Doctrines': 'http://www.kaltura.com/tiny/efy8y',
    'List': 'http://www.kaltura.com/tiny/6tepq',
    'Clustering': 'http://www.kaltura.com/tiny/6ln0z',
    'Flag Phrases': 'http://www.kaltura.com/tiny/had4c',
    'Symbolism': 'http://www.kaltura.com/tiny/813j8',
    'Visualization': 'http://www.kaltura.com/tiny/evnm9',
    'Cause & Effect': 'http://www.kaltura.com/tiny/ez87w'
}


with st.container():
    for key, value in urls.items():
        st.markdown(f'{key}: {value}')

