from mods.base import *
from mods.utils import *

SIDEBAR = 'collapsed'

PAGE_HEADER = 'Reddit Clone App'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'Add a Post'

st.title(SITE_TITLE)
st.subheader(PAGE_SUBHEADER)

# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
# Check for logged in
if st.session_state.username == '':
    st.switch_page('pages/010_Login.py')
else:
    st.sidebar.write(f"You are logged in as {st.session_state.username}")
    if st.sidebar.button('View All Posts'):
        st.switch_page('Home.py') 
    with st.form("post_form"):
        title = st.text_input("Title", value="My Rush Blog App")
        content = st.text_area("Content", value="This app is a place for the Rush family to discuss whatever they need to in total privacy.", height=100)
        # TODO: GET AUTHOR FROM LOGIN INFO
        author = st.text_input("Author", value="drushlopez")
        url = st.text_input("Link URL", value="https://rushblog.streamlit.app")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp", "gif"])
        submitted = st.form_submit_button("Submit")
        if uploaded_file is not None:
            # Save the uploaded image
            image = save_uploaded(uploaded_file, UPLOAD_FOLDER)
            # Display the image
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            st.write("Uploaded image:")
            st.image(file_path, width=50)
            if submitted and image:
                add_record(goals, )
    st.divider()

    # call_back = None
    # button_text = ':scroll:  Add Post'
    # form_name = 'posts_form'       
    # create_form(post_form_inputs, button_text, form_name, True, call_back=call_back)
    # form_inputs_name = f'{form_name}_inputs'       
    # if st.session_state[form_inputs_name]:
    #     save_record(st.session_state[form_inputs_name], form_name)
    # st.divider()



