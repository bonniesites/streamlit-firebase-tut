import streamlit as st

st.title("Log In ")
st.divider()
# st.sidebar.title("Log In ")
# st.divider()

utils.create_form(login_inputs, 'Log in', 'logins')    
st.divider()

# If  logged in/auth, go to Home

# Check for authenticated/logged in

# Else, not logged in, show login screen with signup button

