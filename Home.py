# From https://discuss.streamlit.io/t/streamlit-firestore/9224
# From https://blog.streamlit.io/streamlit-firestore/

import streamlit as st
import os
from PIL import Image
#import mods.base
from mods import dbconnect, base
db = dbconnect.db

st.title('I Read It! Did You?')
st.divider()

def convert_folder_to_webp(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Only convert image files with extensions .png, .jpg, or .jpeg
                image_path = os.path.join(root, file)
                output_folder = os.path.join(root, 'webp')
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.webp')
                im = Image.open(image_path)
                im.save(output_path, 'webp')

# Example usage
#convert_folder_to_webp(img_folder)

def create_form(inputs, prompt, form_name):
    #form_name = ':female-technologist:' + form_name
    with st.expander(prompt):
        # Create a form using a for loop
        # TODO: Input sanitization and validation, required fieldsfrom mods import dbconnect
        with st.form(form_name):
            fields = {}
            for key, value in inputs.items():
                if key == 'username':
                    document_title = key
                elif key == 'post_title':
                    document_title = key
                value_type = type(value)
                if value_type == int:
                    inputs[key] = st.slider(f'{value}', 0, 100, 0)
                elif value_type == str:
                    inputs[key] = st.text_input(f'{value}', '')
                # Add more conditions for other value types as needed
                
            uploaded = st.file_uploader('Upload your pic(s) here...', type=['png', 'jpeg', 'jpg'])

            process_img(uploaded)
            
            submitted = st.form_submit_button(prompt)
            # Once the user has submitted, upload it to the database
            if submitted:
                # Display the submitted data
                st.write('You entered the following information:', inputs)
                save_record(inputs, form_name)
                

# Adapted from                
def process_img(uploaded):
    if uploaded is not None:
        file_details = {'FileName':uploaded.name,'FileType':uploaded.type}
        st.write(file_details)
        img = load_image(uploaded)
        st.image(img,height=250,width=250)
        with open(os.path.join('tempDir',uploaded.name),'wb') as f: 
            f.write(uploaded.getbuffer())         
        st.success(':tada:  Saved image!')
        convert_folder_to_webp('tempDir')
                        
            
def save_record(inputs, form_name):
    #st.write(inputs)
    # TODO: set up authentication/login
    # TODO: sanitize and verify inputs
    # TODO: escape outputs(document_id)     
    #st.toast(':sparkles: Record saved! :white_check_mark:')
    #st.write(doc_ref)
    try:
        doc_ref = db.collection(form_name).add(inputs)    
        document_id = doc_ref[-1].id
        st.write(f'document_id: {document_id}')
        new_doc = db.collection(form_name).document            
        doc_ref.document(document_id).add({'entered' : datetime.datetime.now(tz=datetime.timezone.utc)})
        if form_name == 'posts':
            doc_ref.document(document_id).add({'img' : image_})          
        st.toast(':sparkles: Record saved! :white_check_mark:')
        st.balloons()
    except:
        st.toast(f':fire: Record not saved! :fire:')    
    # finally:        
    #     st.balloons()
    
def delete_record(table, record_id):
    db.collection(table).document(record_id).delete()
    

def edit_record(table, record_id):
    pass

with st.sidebar:
    login_inputs = {
        'login_username': 'Username or email',
        'password': 'Password'
    }
    
    post_inputs = {
        'post_title': 'Post title:',
        'post_content': 'Post content:',
        'post_url': 'Link URL:',
        'post_author': 'username-from-login-session',
        'post_image': ''
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
        'avatar': 'Avatar'
        }    
    
    create_form(login_inputs, 'Log in', 'logins')    
    st.divider()
        
    create_form(post_inputs, ':scroll:  Add a Post', 'posts')
    st.divider()
        
    create_form(user_inputs, 'Add a user', 'users')

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