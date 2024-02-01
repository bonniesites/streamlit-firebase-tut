# From 
# https://discuss.streamlit.io/t/streamlit-firestore/9224
# Part 1: https://blog.streamlit.io/streamlit-firestore/
# Part 2: https://blog.streamlit.io/streamlit-firestore-continued/
# Part 3: https://discuss.streamlit.io/t/streamlit-firestore-continued/12135

from mods.base import *

PAGE_HEADER = 'Reddit Clone App'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'I Read It! Did You?'

st.title(SITE_TITLE)
st.divider()      
st.subheader(PAGE_SUBHEADER)

#  TODO: form to add a category
#  TODO: form for admin to add users 
#  TODO: populate dropdown from db in streamlit

view_posts()    

