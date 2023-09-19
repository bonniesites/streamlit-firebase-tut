import streamlit as st
from mods import utils, base, dbconnect
from mods import calc_functions as cf

page_title = 'Calculus Functions'
page_layout = 'wide'
page_icon = '💫'
sidebar = 'collapsed'
menu_items = {
       'Get Help': 'https://my-reddit.streamlit.app/',
       'Report a bug': 'https://my-reddit.streamlit.app/',
       'About': '# This is a header. '
}

st.title(page_title)
st.header('Pages')

with st.container():
    leftcol, midcol, rightcol = st.columns(3)   
    

    with leftcol:
        link = 'http://localhost:8035/Trig'            
        link_text = 'Trig'
        utils.create_button(link, link_text)
             
        if st.button('Logarithms','Logarithms'):
            st.experimental_set_query_params(page="calculus/")  
        
    with midcol:        
        if st.button('Limits','Limits'):
            st.experimental_set_query_params(page="calculus/")
            
        if st.button('Continuity','Continuity'):
            st.experimental_set_query_params(page="calculus/")
        
    with rightcol: 
        if st.button('Exponents','Exponents'):
            st.experimental_set_query_params(page="calculus/")
             
        if st.button('Derivatives','Derivatives'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('Differentiation','Differentiation'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('Rate of Change','RateofChange'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('Theorems','Theorems'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('Concavity','Concavity'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('Applied Optimization','AppliedOptimization'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('AntiDerivative','AntiDerivative'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('Integrals','Integrals'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('U-Substitution','U-Substitution'):
            st.experimental_set_query_params(page="calculus/") 
        if st.button('Volume','Volume'):
            st.experimental_set_query_params(page="calculus/")
            
  
with st.container():
    st.divider()    
    st.subheader('Logs and Exponents')
    call_back = None
    button_text = 'Calculate'
    form_name = 'cfv_form'
    form_inputs_name = f'{form_name}_inputs'
    st.write(f'form_inputs_name: {form_inputs_name}')   
    utils.create_form(base.cfv_inputs, button_text, form_name, False, call_back)     
    if st.session_state[form_inputs_name]:
        st.write(st.session_state[form_inputs_name])
        result = cf.calc_cfv(st.session_state[form_inputs_name].present, st.session_state[form_inputs_name].rate, st.session_state[form_inputs_name].time)
        st.subheader(f'Result: ${result}')
    st.divider()
    
    