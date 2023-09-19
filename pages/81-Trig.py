import streamlit as st
from fractions import Fraction
import numpy as np
from math import cos, sin, tan, acos, asin, atan
from mods import calc_functions as cf
from mods import utils, base

page_title = 'Trig Functions'
page_layout = 'wide'
page_icon = '💫'
sidebar = 'collapsed'
menu_items = {
       'Get Help': 'https://my-reddit.streamlit.app/',
       'Report a bug': 'https://my-reddit.streamlit.app/',
       'About': '# This is a header. '
}

st.title(page_title)
st.header('Trig')
st.divider()


trig_funcs = {}
for theta in cf.unit_circle:
    radians = np.deg2rad(theta)
    radians_pi = cf.create_rad_symbol(theta)
    hyp = cf.radius
    opp_angle = theta 
    right_angle = 90
    adj_angle = 90 - theta
      
    # st.subheader(f'radians: {radians}')    
    # st.subheader(f'np.sin(radians): {np.sin(radians)}')

    xcos = np.cos(radians)        
    ysin = np.sin(radians)
    tan = cf.calc_trig_function(ysin, xcos)
    sec = cf.calc_trig_function(1, xcos)
    csc = cf.calc_trig_function(1, ysin)
    cot = cf.calc_trig_function(1, tan)
    if theta == 0.0:
        ysin = 0.0
    if theta == 90 or theta == 270:
        tan = 'undefined'
        sec = 'undefined'
    if theta == 180 or theta == 360:
        cot = 'undefined'
        csc = 'undefined'
    
    cos_sym = cf.convert_to_symbols(xcos)
    sin_sym = cf.convert_to_symbols(ysin)
    tan_sym = cf.convert_to_symbols(tan)
    sec_sym = cf.convert_to_symbols(sec)
    csc_sym = cf.convert_to_symbols(csc)
    cot_sym = cf.convert_to_symbols(cot)
    
    new_angle = {
        'theta': theta,
        'radians': radians_pi,
        'cos': xcos,
        'sin': ysin,
        'tan': tan,
        'sec': sec,
        'csc': csc,
        'cot': cot,
        'cos_sym': cos_sym,
        'sin_sym': sin_sym,
        'tan_sym': tan_sym,
        'sec_sym': sec_sym,
        'csc_sym': csc_sym,
        'cot_sym': cot_sym
        } 
    
    trig_funcs[theta] = new_angle
        

with st.container():
    st.subheader('Unit Circle Values')
    # Unit Circle Calculations
    deg_col, rad_col, cos_col, sin_col, tan_col, sec_col, csc_col, cot_col = st.columns(8)

    with deg_col:
        'Degrees'    
    with rad_col:
        'Radians'       
    with sin_col:
        'Sine'           
    with cos_col:
        'Cosine'      
    with tan_col:
        'Tangent'       
    with csc_col:
        'Cosecant'       
    with sec_col:
        'Secant'          
    with cot_col:
        'Cotangent'
    for degree, angle_data in trig_funcs.items():
            # Display
            with deg_col:
                st.write(str(degree))
            with rad_col:
                st.write(angle_data["radians"])
            # Sine
            with sin_col:              
                st.write(angle_data['sin_sym'])
            # Cosine
            with cos_col:                
                st.write(angle_data['cos_sym'])             
            # Tangent
            with tan_col:                
                st.write(angle_data['tan_sym'])
            # Cosecant
            with csc_col:                
                st.write(angle_data['csc_sym'])     
            # Secant
            with sec_col:                
                st.write(angle_data['sec_sym'])        
            # Cotangent
            with cot_col:                
                st.write(angle_data['cot_sym'])
                    


    for degree, angle_data in trig_funcs.items():
        #pass    
        st.write(f'{degree}')
        st.write(f'{angle_data["radians"]}')
        st.write(f'{angle_data["cos"]}')
        st.write(f'Sine: {angle_data["sin"]}')
        st.write(f'Tangent: {angle_data["tan"]}')
        st.write(f'Secant: {angle_data["sec"]}')
        st.write(f'Cosecant: {angle_data["csc"]}')
        st.write(f'Cotangent: {angle_data["cot"]}')
        st.write(f'Cosine Symbolic: {angle_data["cos_sym"]}')
        st.write(f'Sine Symbolic: {angle_data["sin_sym"]}')
        st.write(f'Tangent Symbolic: {angle_data["tan_sym"]}')
        st.write(f'Secant Symbolic: {angle_data["sec_sym"]}')
        st.write(f'Cosecant Symbolic: {angle_data["csc_sym"]}')
        st.write(f'Cotangent Symbolic: {angle_data["cot_sym"]}')
        st.write('-' * 40)