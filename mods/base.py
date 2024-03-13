import streamlit as st
from fractions import Fraction
import numpy as np
import sys
import os
import re
import pandas as pd 
import plotly.express as px 
from PIL import Image
from math import cos, sin, tan, acos, asin, atan, gcd
from fuzzywuzzy import process
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests
from io import BytesIO
from datetime import datetime
from bson import ObjectId
from streamlit_modal import Modal
import streamlit.components.v1 as components
from difflib import get_close_matches

from pydantic import BaseModel, EmailStr, constr, ValidationError
import pydantic_settings
import streamlit_pydantic as sp

# import matplotlib.pyplot as plt
# import sympy as sym
# #sym.init_printing(use_unicode=True)
# sym.init_session()

# TODO: Hide menu until logged in/authenticated, then show menu

PAGE_HEADER = ''
PAGE_SUBHEADER = ''
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'

UPLOAD_FOLDER = '/data/app/uploaded_files'

# Site Constants
PAGE_LAYOUT = 'wide'
PAGE_ICON = '💫'
SIDEBAR = 'expanded'
MENU_ITEMS = {
       'Get Help': 'https://my-reddit.streamlit.app/',
       'Report a bug': 'https://my-reddit.streamlit.app/',
       'About': '# This is a header.'
}

st.set_page_config(page_title=SITE_TITLE, layout=PAGE_LAYOUT, page_icon=PAGE_ICON, initial_sidebar_state=SIDEBAR, menu_items=MENU_ITEMS)

       
# TODO: if logged in, show logout button
if st.sidebar.button("Logout"):
    logout()

css = '''
<style>
       .stDeployButton {visibility: hidden;}
    [data-testid="stSidebar"]{
        min-width: 0px;
        max-width: 350px;
    }
</style>
'''
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

# Global variables

goal_form_inputs = {
       'goal_title':{'type':'text', 'label':'Goal text', 'required':True, 'pattern':''},
       'goal_done':{'type':'toggle', 'label':'Goal Done'},
       'goal_url':{'type':'text', 'label':'Link URL'},
       'goal_image':{'type':'upload', 'label':'Choose icon'},
       'goal_cat':{'type':'text', 'label':'Goal category'},
       'goal_due_date':{'type':'date', 'label':'Due Date'}
}

post_form_inputs = {
       'post_title':{'type':'text', 'label':'Post title'},
       'post_content':{'type':'textarea', 'label':'Post content'},
       'post_url':{'type':'text', 'label':'Link URL'},
       'post_image':{'type':'text', 'label':'Image location'},
       'post_cat':{'type':'select', 'label':'Post category'}
}

user_form_inputs = {
       'username':{'type':'text', 'label':'Username', 'required':True,
        'pattern':''},
       'first':{'type':'text','label':'First name'},
       'last':{'type':'text','label':'Last name'},
       'email':{'type':'text','label':'Email'},
       'street_address':{'type':'text','label':'Street address'},
       'postal_code':{'type':'text','label':'Postal/zip code'},
       'phone':{'type':'text','label':'Phone number'},
       'month':{'type':'text','label':'Birthday month'},
       'day':{'type':'text','label':'Birthday day'},
       'avatar':{'type':'image','label':'Avatar'}
}

# cfv_form_inputs = [
#        'present':'Present value'
#        ,'rate': 'Interest Rate'
#        ,'time': 'Time'
#        #,'period': 'Period'
# ]


# vendor_form_inputs = [
#        'company': 'Company name',
#        'contact_first': 'First name',
#        'contact_last': 'Last name',
#        'email': 'Email',
#        'street_address': 'Street address',
#        'postal_code': 'Postal/zip code',
#        'phone': 'Phone number',
#        'url': 'Website URL address',
#        'day': 'Birthday day',
#        'avatar': 'Logo'
# ]

# cost_form_inputs = [
#        'vendorID': 'Vendor', # use select drawing from vendors collection, also have Add New button
#        'product': 'Product',  # use select from products collection, also have Add New button
#        'unit_name': 'Unit name',
#        'units': 'Number of units', # use slider?
#        'street_address': 'Street address',
#        'postal_code': 'Postal/zip code',
#        'phone': 'Phone number',
#        'month': 'Birthday month',
#        'day': 'Birthday day',
#        'avatar': 'Avatar'
# ]
