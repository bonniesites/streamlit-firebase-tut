from mods.base import *
from mods.utils import *



# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
# Check for logged in
if st.session_state.username == '':
    switch_page('login')
else:
    st.sidebar.write(f"You are logged in as {st.session_state.username}")