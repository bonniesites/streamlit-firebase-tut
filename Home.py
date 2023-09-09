# From https://discuss.streamlit.io/t/streamlit-firestore/9224
# From https://blog.streamlit.io/streamlit-firestore/

import streamlit as st
import os
from PIL import Image
from mods import dbconnect, base, utils

db = dbconnect.get_db()
login_inputs = base.login_inputs
post_inputs = base.post_inputs
user_inputs = base.user_inputs


# TODO: set variable in each page for title, base holds the header code and uses each page's title variable
st.title('I Read It! Did You?')
st.divider()

with st.sidebar:
        
    utils.create_form(post_inputs, ':scroll:  Add a Post', 'posts')
    st.divider()

# Then query to list all users
users_ref = db.collection('users')
users = users_ref.stream()

## for user in users:
#     st.subheader('Users:')
#     print(f'{user.id} => {user.to_dict()}')
    
# And then render each post, using some light Markdown
posts_ref = db.collection('posts')
#posts = posts_ref.stream()
query = posts_ref
#st.write(query.get())

title, title_sort, date_sort, blank_sort = st.columns(4)
with title:        
    st.header('Posts')
with title_sort:
    if st.button('Sort by Title', 'title_sort'):        
        query = posts_ref.order_by('post_title')
with date_sort:
    if st.button('Sort by Date', 'date_sort'):        
        query = posts_ref.order_by('enter_date')
with blank_sort:
    if st.button('', 'blank_sort'):        
        pass        
st.divider()
counter = 0

posts = query.get()
for post in posts:
    record_id = post.id
    counter += 1
    post = post.to_dict()
    title = post['post_title']
    url = post['post_url']
    author = post['post_author']
    content = post['post_content']
    img = post['post_image']
    with st.container():
        title_col, link_col, reply_col, del_col, edit_col = st.columns(5)                  
        with reply_col: 
            if st.button('Reply', 'reply' + str(counter)):
                with st.form():
                    create_form(post_inputs, ':scroll:  Send Reply', 'replies')
        with del_col:
            if st.button('Delete', 'del' + str(counter)):
                delete_record('posts', record_id)
                st.toast(':sparkles:  Post deleted!  :white_check_mark:')
                #st.error(':sparkles: Post deleted! :white_check_mark:')
                #st.balloons()
                # TODO: reload list        
        with edit_col:
            if st.button('Edit', 'edit' + str(counter)):
                edit_record('posts', record_id)
                st.error(':sparkles: Post updated! :white_check_mark:')
                st.balloons()                  
        with title_col: 
            st.subheader(f'{title} ')
        with link_col:
            st.write(f':link: [{url}]({url})')        
        #st.image(img)
        st.write(f'{content}  Author: {author}')        
    st.divider()