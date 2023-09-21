SIDEBAR = 'collapsed'
PAGE_HEADER = 'Add a Post'
PAGE_SUBHEADER = ''

from mods.base import *

post_inputs = post_inputs



call_back = None
button_text = ':scroll:  Add Post'
form_name = 'posts_form'       
create_form(post_inputs, button_text, form_name, True, call_back=call_back)
form_inputs_name = f'{form_name}_inputs'       
if st.session_state[form_inputs_name]:
    save_record(st.session_state[form_inputs_name], form_name)
st.divider()