import streamlit as st
from PIL import Image
# import streamlit.components.v1 as components
# from fractions import Fraction
# import numpy as np
# import sys
# import os
# import re
# import pandas as pd 
# from math import cos, sin, tan, acos, asin, atan, gcd
# from fuzzywuzzy import process
# import requests
# from transformers import pipeline
# from io import BytesIO
# from difflib import get_close_matches
# import logging
# from time import sleep, time
from datetime import datetime, timedelta
from mods.test_data import test_data as td
from bs4 import BeautifulSoup
# from typing import Annotated

# import sympy as sym
# #sym.init_printing(use_unicode=True)
# sym.init_session()
# 
# 

UPLOAD_FOLDER = '/data/app/uploaded_files'

PAGE_LAYOUT = 'wide'
PAGE_ICON = Image.open("./favicon.ico")
SIDEBAR = 'expanded'

# APP VARIABLES
PAGE_HEADER = ''
PAGE_SUBHEADER = ''
SITE_TITLE = 'My SMART Goals Journal'
PAGE_TITLE = f'{SITE_TITLE} | {PAGE_HEADER} {PAGE_SUBHEADER}'


st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT, page_icon=PAGE_ICON, initial_sidebar_state=SIDEBAR)
st.title(PAGE_TITLE)  # browser tab display

if 'count' not in st.session_state:
       st.session_state.count = ''

if 'results' not in st.session_state:
       st.session_state.results = ''

# TODO: Remove hardcoded username, get from login info
if 'username' not in st.session_state:
    # st.session_state.username = ''
    st.session_state.username = 'drl2'    

if "user_role" not in st.session_state:
    st.session_state.user_role = ''

if 'filter_option' not in st.session_state:
       st.session_state.filter_option = {}

if 'sort' not in st.session_state:
       st.session_state.sort = {}

if 'sort_order' not in st.session_state:
       st.session_state.sort_order = -1
print(f'\n\n {st.session_state.sort_order} \n\n')


css = '''
<style>
       .reportview-container 
       {
            margin-top: -2em;
        }
       #stDecoration, .stDeployButton
       {
        max-width: 0px;
        display: none important!;
        visibility: hidden important!;
       }
</style>
'''
#st.write('after css')
# st.markdown("""
#     <style>
#         .reportview-container {
#             margin-top: -2em;
#         }
#         #MainMenu {visibility: hidden;}
#         .stDeployButton {display:none;}
#         footer {visibility: hidden;}
#         #stDecoration {display:none;}
#     </style>
# """, unsafe_allow_html=True)

st.markdown(css, unsafe_allow_html=True)

## This goes in the custom format as a new line after debugging: 
## footer {visibility: hidden;}
custom_format = '''
       <style>
       #root {background-image: url('https://images.unsplash.com/photo-1688453756951-842a78eec6ad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2535&q=80');
       background-size: cover;}
       </style>
       '''
st.markdown(custom_format, unsafe_allow_html=True)

# st.write('after custom_format')    
# TODO: Setup user roles/permissions in pydantic models
# Check for logged in
if not st.session_state.username == '' and not st.session_state.username == None:
    USER_NAME = st.session_state.get('username')
    if USER_NAME == 'drl2':
       st.session_state.user_role = 'admin'
    st.sidebar.write(f'Logged in as {USER_NAME}')         
    if st.sidebar.button("Logout"):
        logout()
else:
    # pass
    st.write('switching to Login page')  
    st.switch_page('pages/010_Login.py')
