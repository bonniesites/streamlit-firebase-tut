import streamlit as st
from mods import base
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
        st.subheader(f'{key}: {value}', divider=False)

