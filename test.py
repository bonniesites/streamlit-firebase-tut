import streamlit as st
from datetime import datetime, timedelta
from time import sleep
from mods import test_data as td
import os
from PIL import Image

from mods.base import *
from mods.utils import *


PAGE_HEADER = ''
PAGE_SUBHEADER = ''
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'

UPLOAD_FOLDER = '/data/app/uploaded_files'

# Site Constants
PAGE_LAYOUT = 'wide'
PAGE_ICON = Image.open("./favicon.ico")
SIDEBAR = 'expanded'

st.set_page_config(page_title=SITE_TITLE, layout=PAGE_LAYOUT, page_icon=PAGE_ICON, initial_sidebar_state=SIDEBAR, menu_items=MENU_ITEMS)


MENU_ITEMS = {
       'Get Help': 'https://my-reddit.streamlit.app/',
       'Report a bug': 'https://my-reddit.streamlit.app/',
       'About': '# This is a header.'
}

COUNTER = 1

message_container = st.empty()
sidebar_msg = st.sidebar.empty()
addgoal_form_container = st.sidebar.empty()

# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())

modal_add_goal = st.popover('Add a goal')

with modal_add_goal:
    # Form to add new goal
    with st.form(key='new_goal_form'):
        # Get data inputs
        category = st.text_input('Category')
        goal_task = st.text_input('Goal Task')
        duedate = st.date_input('Due Date', value=datetime.now() + timedelta(days=1))
        # Submit button
        submitted = st.form_submit_button('Save Goal', type='primary', help="Save the new goal")
        if submitted:
            message_container.success(f'submitted: {submitted},\n duedate: {duedate},\n timestamp: {datetime.now()},\n category: {category},\n goal_task: {goal_task} ')
            #duedate = date_to_datetime(duedate)
            goal_data = {'timestamp': datetime.now(), 'category': category, 'goal': goal_task, 'duedate': date_to_datetime(duedate), 'is_done': False }
            submit_result = add_new_document(GOALS, goal_data)
            sidebar_msg.success("Document inserted successfully with id:", submit_result.inserted_id)
            sleep(3)
            if submit_result:
                st.rerun()
                sidebar_msg.success("Document inserted successfully with id:", submit_result.inserted_id)
                sleep(3)                
            else:
                sidebar_msg.warning("Failed to insert document.")
                sleep(3)


modal_edit_goal = st.popover('Edit a goal')

with modal_edit_goal:
    # Form to edit goal
    with st.form(key='edit_goal_form'):
        # Get data inputs
        category = st.text_input('Category')
        goal_task = st.text_input('Goal Task')
        duedate = st.date_input('Due Date', value=datetime.now() + timedelta(days=1))
        # Submit button
        get_goal_info = st.form_submit_button('Edit Goal', type='primary', help="Edit the goal")
        if get_goal_info:
            message_container.success(f'get_goal_info: {get_goal_info},\n duedate: {duedate},\n timestamp: {datetime.now()},\n category: {category},\n goal_task: {goal_task} ')
            #duedate = date_to_datetime(duedate)
            new_data = {'timestamp': datetime.now(), 'category': category, 'goal': goal_task, 'duedate': date_to_datetime(duedate), 'is_done': False }
            submit_result = add_new_document(GOALS, goal_data)
            sidebar_msg.success("Document inserted successfully with id:", submit_result.inserted_id)
            sleep(3)
            if submit_result:
                st.rerun()
                sidebar_msg.success("Document inserted successfully with id:", submit_result.inserted_id)
                sleep(3)                
            else:
                sidebar_msg.warning("Failed to insert document.")
                sleep(3)
    
                
if 'sum' not in st.session_state:
    st.session_state.sum = ''

col1,col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

    with st.form('addition'):
        a = st.number_input('a')
        b = st.number_input('b')
        submit = st.form_submit_button('add')

    # The value of st.session_state.sum is updated at the end of the script rerun,
    # so the displayed value at the top in col2 does not show the new sum. Trigger
    # a second rerun when the form is submitted to update the value above.
    st.session_state.sum = a + b
    if submit:
        st.rerun()
