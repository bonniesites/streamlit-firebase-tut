import streamlit as st
from fractions import Fraction
import numpy as np
import sys
import os
import re
from PIL import Image
from math import cos, sin, tan, acos, asin, atan, gcd
from fuzzywuzzy import process
from pymongo import MongoClient
import requests
from io import BytesIO
from datetime import datetime
from bson import ObjectId
from streamlit_modal import Modal
import streamlit.components.v1 as components

# import matplotlib.pyplot as plt
# import sympy as sym
# #sym.init_printing(use_unicode=True)
# sym.init_session()


PAGE_HEADER = ''
PAGE_SUBHEADER = ''
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'

UPLOAD_FOLDER = '/data/uploaded_files'

#from mods.dbconnect import *
from mods.utils import *

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

css = '''
<style>
    [data-testid="stSidebar"]{
        min-width: 0px;
        max-width: 450px;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

## This goes in the custom format as a new line after debugging: 
## footer {visibility: hidden;}
custom_format = '''
       <style>
       .stDeployButton {visibility: hidden;}
       #root {background-image: url('https://images.unsplash.com/photo-1688453756951-842a78eec6ad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2535&q=80');
       background-size: cover;}
       </style>
       '''
st.markdown(custom_format, unsafe_allow_html=True)

# Global variables

login_form_inputs = {
       'login_username': 'Username or email',
       'password': 'Password'
}

post_form_inputs = {
       'post_title': 'Post title',
       'post_content': 'Post content',
       'post_url': 'Link URL',
       'post_author': 'username-from-login-session',
       'post_image': 'Image location',
       'post_cat': 'Post category'
}

user_form_inputs = {
       'username': 'Username',
       'first': 'First name',
       'last': 'Last name',
       'email': 'Email',
       'street_address': 'Street address',
       'postal_code': 'Postal/zip code',
       'phone': 'Phone number',
       'month': 'Birthday month',
       'day': 'Birthday day',
       'avatar': 'Avatar'
}

cfv_form_inputs = {
       'present': 'Present value'
       ,'rate': 'Interest Rate'
       ,'time': 'Time'
       #,'period': 'Period'
}


vendor_form_inputs = {
       'company': 'Company name',
       'contact_first': 'First name',
       'contact_last': 'Last name',
       'email': 'Email',
       'street_address': 'Street address',
       'postal_code': 'Postal/zip code',
       'phone': 'Phone number',
       'url': 'Website URL address',
       'day': 'Birthday day',
       'avatar': 'Logo'
}

cost_form_inputs = {
       'vendorID': 'Vendor', # use select drawing from vendors collection, also have Add New button
       'product': 'Product',  # use select from products collection, also have Add New button
       'unit_name': 'Unit name',
       'units': 'Number of units', # use slider?
       'street_address': 'Street address',
       'postal_code': 'Postal/zip code',
       'phone': 'Phone number',
       'month': 'Birthday month',
       'day': 'Birthday day',
       'avatar': 'Avatar'
}


# TODO: Hide menu until logged in/authenticated, then show menu

# Check for authenticated/logged in

# Not logged in, show login screen with signup button

# Signup button goes to signup page

