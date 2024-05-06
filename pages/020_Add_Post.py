PAGE_HEADER = 'Reddit Clone App'
PAGE_SUBHEADER = 'Add a Post'
SITE_TITLE = f'My Multi App | {PAGE_HEADER} | {PAGE_SUBHEADER}'

from mods.header import * 
from mods.models import *
from mods.data_processing import *
from mods.utils import *
import os

st.header(SITE_TITLE)

if st.sidebar.button('View All Posts'):
    st.switch_page('Home.py') 
with st.form("add_post_form"):
    title = st.text_input("Title", value="My Reddit Clone App")
    content = st.text_area("Content", value="This app is a place for the Rush family to discuss whatever they need to in total privacy.", height=100)
    # TODO: GET AUTHOR FROM LOGIN INFO
    author = st.text_input("Author", value=st.session_state.username)
    url = st.text_input("Link URL", value="https://rushblog.streamlit.app")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "gif"])
    file_path = ''
    save_post = st.form_submit_button("Save Post")
    if uploaded_file is not None:
        # Save the uploaded image
        image = save_uploaded(uploaded_file, UPLOAD_FOLDER)
        # Display the image
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        st.write("Uploaded image:")
        st.image(file_path, width=50)
    new_post = {
        "post_timestamp": datetime.utcnow(),
        'post_title': title,
        'post_content': content, 
        "post_author": st.session_state.username,
        'post_img': file_path,
        'post_url': url
    }        
    if save_post:
        add_post(new_post)
        
st.divider()

# call_back = None
# button_text = ':scroll:  Add Post'
# form_name = 'posts_form'       
# create_form(post_form_inputs, button_text, form_name, True, call_back=call_back)
# form_inputs_name = f'{form_name}_inputs'       
# if st.session_state[form_inputs_name]:
#     save_record(st.session_state[form_inputs_name], form_name)
# st.divider()



