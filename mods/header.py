import streamlit as st
import streamlit.components.v1 as components
from fractions import Fraction
import numpy as np
import sys
import os
import re
import pandas as pd 
from PIL import Image
from math import cos, sin, tan, acos, asin, atan, gcd
from fuzzywuzzy import process
import requests
from transformers import pipeline
from io import BytesIO
from difflib import get_close_matches
import logging
from time import sleep, time
from datetime import datetime, timedelta
from mods import test_data as td
from typing import Annotated
import threading
# import sympy as sym
# #sym.init_printing(use_unicode=True)
# sym.init_session()

PAGE_HEADER = ''
PAGE_SUBHEADER = ''
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'

UPLOAD_FOLDER = '/data/app/uploaded_files'

# Site Constants
PAGE_LAYOUT = 'wide'
#PAGE_ICON = Image.open("./favicon.ico")
PAGE_ICON = None
SIDEBAR = 'expanded'

st.set_page_config(page_title=SITE_TITLE, layout=PAGE_LAYOUT, page_icon=PAGE_ICON, initial_sidebar_state=SIDEBAR)

# # Set logging level to DEBUG
# #logging.basicConfig(level=logging.DEBUG)

# TODO: Remove hardcoded username, get from login info
if 'username' not in st.session_state:
    st.session_state.username = ''
    
if "user_role" not in st.session_state:
    st.session_state.user_role = 'admin'
   
if 'popover' not in st.session_state:
    st.session_state.popover = True
    
if 'count' not in st.session_state:
    st.session_state.count = ''
    
if 'results' not in st.session_state:
    st.session_state.results = ''
    
# # TODO: Setup user roles/permissions in pydantic models

# # Check for logged in
# if not st.session_state.username == '':
#     st.sidebar.write(f"You are logged in as {st.session_state.username}")
#     st.switch_page('Home.py')
  
# USER_NAME = st.session_state.username
# # USER_NAME = ''

# # TODO: if logged in, show logout button
# title, logout = st.columns([6, 1])
# with title:
#     SITE_TITLE   
# with logout:
#     user = st.session_state.get('user_name')
#     if USER_NAME is None:
#         USER_NAME = 'drushlopez'
#     st.write(f'Logged in as {USER_NAME}')
    
        
#     if st.button("Logout"):
#         logout()
