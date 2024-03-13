SIDEBAR = 'collapsed'
PAGE_HEADER = 'Edit User'
PAGE_SUBHEADER = ''

from mods.base import *
from mods.utils import *


# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
# Check for logged in
if st.session_state.username == '':
    st.switch_page('pages/010_Login.py')
else:
    st.sidebar.write(f"You are logged in as {st.session_state.username}")