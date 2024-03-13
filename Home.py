# From 
# https://discuss.streamlit.io/t/streamlit-firestore/9224
# Part 1: https://blog.streamlit.io/streamlit-firestore/
# Part 2: https://blog.streamlit.io/streamlit-firestore-continued/
# Part 3: https://discuss.streamlit.io/t/streamlit-firestore-continued/12135

from mods.base import *
from mods.utils import *


PAGE_HEADER = 'Reddit Clone App'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'I Read It! Did You?'

st.title(SITE_TITLE)
st.subheader(PAGE_SUBHEADER)

#  TODO: form to add a category
#  TODO: form for admin to add users 
#  TODO: populate dropdown from db in streamlit - pull qquery and use for options in st.selectbox or st.multiselect


# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''

# Check for logged in
if st.session_state.username != '':
    st.sidebar.write(f"You are logged in as {st.session_state.username}")    
    if st.sidebar.button('+ Add a Post'):
        st.switch_page('pages/020_Add_Post.py') 
    view_posts()
else:
    # Go to Login page
    st.switch_page('pages/010_Login.py')

