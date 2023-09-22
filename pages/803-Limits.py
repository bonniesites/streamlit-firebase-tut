PAGE_HEADER = 'Limits'
PAGE_SUBHEADER = ''
SIDEBAR = 'expanded'
PAGE_LAYOUT = 'wide'

from mods.base import *

with st.sidebar:
    st.header('Limit Laws')
    st.subheader('Basic Limit Law')
    image1 = "pages/img/limit_law1.png"
    image2 = "pages/img/limit_law2.png"
    st.image(image1, caption="", use_column_width=True)
    st.subheader('Other Limit Laws')
    st.image(image2, caption="", use_column_width=True)


with st.container():
    
    st.subheader('Limit Table Calculator')
    with st.container():            
        with st.form('limit_form'):
            st.subheader('Limit by Tables')
            
            eq_top = st.text_input(label='Equation numerator:', value='x ** 2 + 9 * x - 36', max_chars=150, key='eq_up', placeholder='numerator of equation')
            
            eq_bottom = st.text_input(label='Equation denominator:', value='1', max_chars=150, key='eq_down', placeholder='denominator of equation')
            
            limit_num = st.number_input(label='Lim x->:', min_value=-25, max_value=25, value=0, step=1, key='lim_num')
            
            x_value = st.slider(label='x value:', min_value=-25, max_value=25, value=0, step=1, key='x_val')
            
            submitted = st.form_submit_button()
            if submitted:
                st.write(eq_top, eq_bottom, limit_num, x_value)
                allowed_pattern = r'^[xsincot0-9/\+\-=\*\^ \t]+$'                    
                if re.match(allowed_pattern, eq_top):
                    st.write("Numerator valid:", eq_top)
                    if re.match(allowed_pattern, eq_bottom):
                        st.write("Denominator valid:", eq_bottom)
                        process_limit(eq_top, eq_bottom, limit_num, x_value)
                    else:
                        st.write("Denominator invalid. Please enter a valid equation denominator.")
                else:
                    st.write("Numerator invalid. Please enter a valid equation numerator.")
                