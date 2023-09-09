import streamlit as st

st.set_page_config(
       page_title='My Reddit App',
       layout='wide',
       page_icon='💫',
       initial_sidebar_state='expanded',
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

# Global variables

login_inputs = {
       'login_username': 'Username or email',
       'password': 'Password',
}

post_inputs = {
       'post_title': 'Post title:',
       'post_content': 'Post content:',
       'post_url': 'Link URL:',
       'post_author': 'username-from-login-session',
       'post_image': '',
}

user_inputs = {
       'username': 'Username',
       'first': 'First name',
       'last': 'Last name',
       'email': 'Email',
       'street_address': 'Street address',
       'postal_code': 'Postal/zip code',
       'phone': 'Phone number',
       'month': 'Birthday month',
       'day': 'Birthday day',
       'avatar': 'Avatar',
}


# TODO: Hide menu until logged in/authenticated, then show menu

# Check for authenticated/logged in

# Not logged in, show login screen with signup button

# Signup button goes to signup page

