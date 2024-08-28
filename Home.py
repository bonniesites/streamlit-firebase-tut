# Adapted from 
# https://discuss.streamlit.io/t/streamlit-firestore/9224
# Part 1: https://blog.streamlit.io/streamlit-firestore/
# Part 2: https://blog.streamlit.io/streamlit-firestore-continued/
# Part 3: https://discuss.streamlit.io/t/streamlit-firestore-continued/12135


# from mods.imports import *
# from mods.variables import *
# from mods.db import *
from mods.db_functions import *

import streamlit as st

PAGE_SUBHEADER = 'Home'

def get_user(current_user):
    return st.session_state.get('username')

def get_user_role(current_user):
    return st.session_state.get('user_role')

st.header(f'{PAGE_HEADER} | {PAGE_SUBHEADER}')

#  TODO: form to add a category
#  TODO: form for admin to add users 
#  TODO: populate dropdown from db in streamlit - pull qquery and use for options in st.selectbox or st.multiselect 

print('inside Home.main()')
addgoal, view_all, view_done, view_open = st.columns(4)
with addgoal:  
    pass
    #add_goal()          
            
with view_all:
    allgoals = st.button('View All', type='primary')
    if allgoals:
        #custom_print('inside Home.allgoals button')
        st.switch_page('pages/0000_All_Goals.py')
with view_done:
    donegoals = st.button('View Done', type='primary')
    if donegoals:
        #custom_print('inside Home.donegoals button')
        st.switch_page('pages/0002_Done.py')
with view_open:
    opengoals = st.button('View Open', type='primary')
    if donegoals:
        #custom_print('inside Home.opengoals button')
        st.switch_page('pages/0004_Open.py')


print('end Home.main()')