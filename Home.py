# Adapted from 
# https://discuss.streamlit.io/t/streamlit-firestore/9224
# Part 1: https://blog.streamlit.io/streamlit-firestore/
# Part 2: https://blog.streamlit.io/streamlit-firestore-continued/
# Part 3: https://discuss.streamlit.io/t/streamlit-firestore-continued/12135

import threading

PAGE_HEADER = 'Home'
PAGE_SUBHEADER = ''
from mods.header import *
# from mods.models import *
from mods.data_processing import *
from mods.utils import *

def get_user(current_user):
    return st.session_state.get('username')

def get_user_role(current_user):
    return st.session_state.get('user_role')

st.header(SITE_TITLE)

#  TODO: form to add a category
#  TODO: form for admin to add users 
#  TODO: populate dropdown from db in streamlit - pull qquery and use for options in st.selectbox or st.multiselect 

#st.write('invoked Home.main()')
addgoal, view_all, view_done, view_open = st.columns(4)
with addgoal:  
    #add_goal()      
    # Create modal (pop up) form
    with st.popover('  \+ &nbsp;&nbsp;  Add &nbsp; :new: &nbsp; goal: &nbsp;&nbsp; \+ '):
        with st.form('add_goal_form'):
            st.write('Add a new goal:')
            category = st.text_input('Category')
            goal_task = st.text_input('Goal Task')
            duedate = date_to_datetime(st.date_input('Due Date', value=datetime.now() + timedelta(days=1)))
            submitted = st.form_submit_button('Save Goal', type='primary', help='Save the new goal info you just entered')
        #submitted = show_form(FORM_CONTAINER, 'Add Goal', 'add_goal', fields, 'Save Goal', 'Save the new goal you entered')
        if submitted:
            #timer = threading.Timer(0.25, close_popover)
            #timer.start()   
            goal_data = {'timestamp': datetime.now(), 'category': category, 'goal_task': goal_task, 'duedate': date_to_datetime(duedate), 'is_done': False }   
            st.write(f'goal_data: {goal_data}')                 
            submit_result = add_new_document(GOALS_LIST, goal_data)  
            st.write(f'submit_result: {submit_result}')           
            
with view_all:
    allgoals = st.button('View All', type='primary')
    if allgoals:
        st.switch_page('pages/001_All_Goals.py')
with view_done:
    donegoals = st.button('View Done', type='primary')
    if donegoals:
        st.switch_page('pages/002_Done.py')
with view_open:
    opengoals = st.button('View Open', type='primary')
    if donegoals:
        st.switch_page('pages/004_Open.py')

