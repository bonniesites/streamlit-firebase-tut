PAGE_HEADER = 'Limits'
PAGE_SUBHEADER = ''
SIDEBAR = 'collapsed'
PAGE_LAYOUT = 'wide'

from mods.base import *

leftcol, midcol, rightcol = st.columns(3)
with st.container():
    with leftcol:
        st.subheader('Limit Laws')
        'Basic Limit Results'
        'For any real number a'
        'and' 
        'any real constant c:'
        f'lim{sym_x}={sym_a}'
        f'{sym_x}→{sym_a}'
        f'lim{sym_x}={sym_a}'
        f'{sym_c}→{sym_c}'
                      
        
    with midcol:
        st.subheader('Examples')
        
        
    with rightcol:
        st.subheader('Calculators')
        with st.container:
            with st.form():
                st.subheader('Limit by Tables')
                st.input_number()
                if st.form_submit_button():
                    pass