from mods.base import *

SIDEBAR = 'collapsed'

PAGE_HEADER = 'Reddit Clone App'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'Add a Post'

st.title(SITE_TITLE)
st.divider()      
st.subheader(PAGE_SUBHEADER)


with st.form("post_form"):
    title = st.text_input("Title", value="My Rush Blog App")
    content = st.text_area("Content", value="This app is a place for the Rush family to discuss whatever they need to in total privacy.", height=100)
    # TODO: GET AUTHOR FROM LOGIN INFO
    author = st.text_input("Author", value="drushlopez")
    url = st.text_input("Link URL", value="https://rushblog.streamlit.app")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "gif"])
    #     st.image(image, caption=uploaded_file.name, width=200)
    # else:
    #     image = ''
    #     st.write("No image uploaded.")
    submitted = st.form_submit_button("Submit")
    if uploaded_file is not None:
        # Save the uploaded image
        image = save_uploaded(uploaded_file, UPLOAD_FOLDER)
        # Display the image
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        st.write("Uploaded image:")
        st.image(file_path, width=50)
        if submitted and image:
            add_post(title, content, author, file_path, url)

st.divider()

# call_back = None
# button_text = ':scroll:  Add Post'
# form_name = 'posts_form'       
# create_form(post_form_inputs, button_text, form_name, True, call_back=call_back)
# form_inputs_name = f'{form_name}_inputs'       
# if st.session_state[form_inputs_name]:
#     save_record(st.session_state[form_inputs_name], form_name)
# st.divider()



