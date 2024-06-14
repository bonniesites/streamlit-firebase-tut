PAGE_HEADER = 'GOALS Clone App'
PAGE_SUBHEADER = 'Login'
SITE_TITLE = f'My Multi App | {PAGE_HEADER} | {PAGE_SUBHEADER}'

from mods.header import *
from mods.data_processing import *
from mods.utils import *
from mods.models import *

st.title(SITE_TITLE)
st.subheader(PAGE_SUBHEADER)

# TODO: CHECK FOR SECURITY!!! Inputs, session, injection, etc.

if 'form' not in st.session_state:
       st.session_state.form = ''

# Initialize Login or Signup forms
if st.session_state.form=='signup_form' and st.session_state.username=='':  
    signup_form = st.form(key='signup_form', clear_on_submit=True)
    new_username = signup_form.text_input(label='Enter Username*')
    new_user_email = signup_form.text_input(label='Enter Email Address*')
    new_user_pas = signup_form.text_input(label='Enter Password*', type='password')
    user_pas_conf = signup_form.text_input(label='Confirm Password*', type='password')
    note = signup_form.markdown('**required fields*')
    signup = signup_form.form_submit_button(label='Sign Up')
    
    if signup:
        if '' in [new_username, new_user_email, new_user_pas, user_pas_conf]:
            st.sidebar.error('Some fields are missing')
        else:
            if GOALS_USERS.find_one({'user' : new_username}):
                st.sidebar.error('Username already exists. Please log in.')
            if GOALS_USERS.find_one({'email' : new_user_email}):
                st.sidebar.error('Email is already registered. Please log in.')
            else:
                if new_user_pas != user_pas_conf:
                    st.sidebar.error('Passwords do not match.')
                else:
                    user_update(new_username)
                    GOALS_USERS.insert_one({'user' : new_username, 'email' : new_user_email, 'pass' : new_user_pas})
                    st.sidebar.success('You have successfully registered!')
                    st.sidebar.success(f"You are logged in as {new_username}")
                    del new_user_pas, user_pas_conf
                    
elif st.session_state.username == '':
    login_form = st.form(key='signin_form', clear_on_submit=True)
    username = login_form.text_input(label='Enter Username', value='drl2')
    user_pas = login_form.text_input(label='Enter Password', type='password')
    
    if GOALS_USERS.find_one({'user' : username, 'pass' : user_pas}):
        login = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        if login:
            st.sidebar.success(f"You are logged in as {username}")
            st.session_state.user['user_name'] = username
            del user_pas
            # Go to Home.py page
            st.switch_page('Home.py')                       
    else:
        login = login_form.form_submit_button(label='Sign In')
        if login:
            st.sidebar.error("Login unsuccessful. Please try again or create an account.")
else:
    logout()

# 'Create Account' button
if st.session_state.username == "" and st.session_state.form != 'signup_form':
    st.subheader('Not a member yet?')
    signup_request = st.button('Create Account', on_click=select_signup)

