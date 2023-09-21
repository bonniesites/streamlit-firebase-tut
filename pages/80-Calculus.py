from mods.base import *


PAGE_HEADER = 'Calculus Functions'
PAGE_SUBHEADER = 'Pages'
MENU_ITEMS = {
       'Get Help': 'https://my-reddit.streamlit.app/',
       'Report a bug': 'https://my-reddit.streamlit.app/',
       'About': '# This is a header. '
}
    
with st.container():
    leftcol, midcol, rightcol = st.columns(3)

    with leftcol:
        for item in calc_menu_left:
            create_button(item, item)
        
    with midcol:
        for item in calc_menu_mid:
            create_button(item, item)
        
    with rightcol:
        for item in calc_menu_right:
            link = item
            link_text = item.replace('_', ' ')
            create_button(link, link_text)
            
  
with st.container():
    st.divider()    
    st.subheader('Logs and Exponents')
    call_back = None
    button_text = 'Calculate'
    form_name = 'cfv_form'
    form_inputs_name = f'{form_name}_inputs'
    st.write(f'form_inputs_name: {form_inputs_name}')   
    create_form(cfv_inputs, button_text, form_name, False, call_back)     
    if st.session_state[form_inputs_name]:
        st.write(st.session_state[form_inputs_name])
        result = calc_cfv(st.session_state[form_inputs_name].present, st.session_state[form_inputs_name].rate, st.session_state[form_inputs_name].time)
        st.subheader(f'Result: ${result}')
    st.divider()
    
    