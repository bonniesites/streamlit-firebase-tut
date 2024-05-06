#PAGE_TITLE = ''
PAGE_HEADER = 'Page Header Here'
PAGE_SUBHEADER = 'Subheader Here'
SIDEBAR = 'collapsed'
# MENU_ITEMS = {
    # 'text': 'link'
# }

from mods.header import *

# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
# Check for logged in
if st.session_state.username == '':
    st.switch_page('pages/010_Login.py')
else:
    st.sidebar.write(f"You are logged in as {st.session_state.username}")
    

