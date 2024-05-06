# From 
# https://discuss.streamlit.io/t/streamlit-firestore/9224
# Part 1: https://blog.streamlit.io/streamlit-firestore/
# Part 2: https://blog.streamlit.io/streamlit-firestore-continued/
# Part 3: https://discuss.streamlit.io/t/streamlit-firestore-continued/12135

import streamlit as st

PAGE_HEADER = 'Reddit Clone App'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'I Read It! Did You?'
SORT_ORDER = -1

from mods.header import *
from mods.models import *
from mods.data_processing import *
# st.write(f"sort_value: {st.session_state.get('sort_value')}")
def get_user(current_user):
    return st.session_state.get('username')

st.title(SITE_TITLE)
st.subheader(PAGE_SUBHEADER)

#  TODO: form to add a category
#  TODO: form for admin to add users 
#  TODO: populate dropdown from db in streamlit - pull qquery and use for options in st.selectbox or st.multiselect   

st.session_state.username = 'drl2'
# Check for logged in user
if not 'username' in st.session_state:
    st.session_state.username = ''
    st.switch_page('pages/010_Login.py')
        

if st.session_state.username != None and st.session_state.username != '':
    st.sidebar.write(f"You are logged in as {st.session_state.username}")    
    if st.sidebar.button('+ Add a Post'):
        st.switch_page('pages/020_Add_Post.py')
        
def fetch_data(collection):
    """Fetches data from MongoDB collection."""
    data = list(collection.find().sort('post_timestamp'))
    return data

def main():

    # st.write(f'REDDIT_DB: {REDDIT_DB}')
  
    # st.write(f'REDDIT_POSTS: {REDDIT_POSTS}') 
    # st.write(f'REDDIT_COMMENTS: {REDDIT_COMMENTS}') 
    # st.write(f'REDDIT_LIKES: {REDDIT_LIKES}') 
    # st.write(f'REDDIT_DISLIKES: {REDDIT_DISLIKES}') 
    # st.write(f'REDDIT_FLAGS: {REDDIT_FLAGS}')

    posts = view_posts({}, 'post_timestamp', -1)
    
    st.title('MongoDB Collection Viewer')
    # Fetch data from MongoDB
    data = fetch_data(REDDIT_POSTS)
    if data:
        # Dynamically create columns based on the first document's keys
        keys = data[0].keys()
        columns = st.columns(len(keys))        
        # Display column headers
        for col, key in zip(columns, keys):
            col.write(key)        
        # Display rows
        for document in data:
            columns = st.columns(len(keys))
            for col, key in zip(columns, keys):
                col.write(document.get(key, ''))
    else:
        st.write("No data found in the collection.")

if __name__ == '__main__':
    main()
else:
    # Go to Login page
    st.switch_page('pages/010_Login.py')





