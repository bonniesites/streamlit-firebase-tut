PAGE_HEADER = 'Limits'
PAGE_SUBHEADER = ''
SIDEBAR = 'expanded'
PAGE_LAYOUT = 'wide'

from mods.base import *

# Symbols:   f 

with st.sidebar:
    st.header('Limit Laws')
    st.subheader('Basic Limit Law')
    image1 = "pages/img/limit_law1.png"
    image2 = "pages/img/limit_law2.png"
    st.image(image1, caption="", use_column_width=True)
    st.subheader('Other Limit Laws')
    st.write('Let f(x) and g(x) be defined over all x≠a over some open interval containing a. ')
    st.image(image2, caption="", use_column_width=True)


with st.container():
    st.subheader('Limit Table Calculator')
    with st.container():            
        with st.form('limit_form'):
            st.subheader('Limit by Tables')
            
            eq_top = st.text_input(label='Equation numerator:', value='(9-7*x)*(sqrt(6-4*x))', max_chars=25, key='eq_up', placeholder='numerator of equation')
            
            eq_bottom = st.text_input(label='Equation denominator:', value='1', max_chars=150, key='eq_down', placeholder='denominator of equation')
            
            limit_num = st.number_input(label='Lim x->:', min_value=-25, max_value=25, value=-3, step=1, key='lim_num')
            
            x_value = st.slider(label='x value:', min_value=-25, max_value=25, value=0, step=1, key='x_val')
            
            submitted = st.form_submit_button()
            if submitted:
                st.write(eq_top, eq_bottom, limit_num, x_value)
                allowed_pattern = r'^[xqrsincot0-9/\+\-=*^\(\)\t]+$'                    
                if regex_matches(allowed_pattern, eq_top):
                    if regex_matches(allowed_pattern, eq_bottom):
                        limit_table(eq_top, eq_bottom, limit_num, x_value)
                                