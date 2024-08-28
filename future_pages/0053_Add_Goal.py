# from mods.header import *
from mods.models import *
from mods.data_processing import *
from mods.utils import *

SIDEBAR = 'collapsed'

PAGE_HEADER = 'My SMART Goals Journal'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'Add a Goal'

st.title(SITE_TITLE)
st.subheader(PAGE_SUBHEADER)


# Example usage for the 'post_form_inputs' model
dynamic_form(goal_form_inputs, 'goals', 'Add a Goal')

# Call dynamic_form with different models and collection names as needed
# dynamic_form(user_form_inputs, , 'Add a User')
# dynamic_form(cfv_form_inputs, "cfvs", 'Add a CFV')
# dynamic_form(vendor_form_inputs, "vendors", 'Add a Vendor')
# dynamic_form(cost_form_inputs, "costs", 'Add a Cost')

# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
# Not logged in
if st.session_state.username == '':
    st.switch_page('pages/010_Login.py')
# Logged in!
else:
    st.sidebar.write(f"You are logged in as {st.session_state.username}")
    with st.form("goal_form"):        
        dynamic_form(goal_form_inputs, 'goals', 'Add a Goal')
        if submitted:
            if uploaded_file is not None:
                # Save the uploaded image
                image = save_uploaded(uploaded_file, UPLOAD_FOLDER)
                # Display the image
                file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
                st.write("Uploaded image:")
                st.image(file_path, width=50)
                if image:
                    add_record(title, cat, file_path, url)
                else:
                    file_path = ''
                    add_record(title, cat, file_path, url)
    st.divider()

    # call_back = None
    # button_text = ':scroll:  Add Post'
    # form_name = 'posts_form'       
    # create_form(post_form_inputs, button_text, form_name, True, call_back=call_back)
    # form_inputs_name = f'{form_name}_inputs'       
    # if st.session_state[form_inputs_name]:
    #     save_record(st.session_state[form_inputs_name], form_name)
    # st.divider()



