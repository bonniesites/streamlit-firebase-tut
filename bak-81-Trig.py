import streamlit as st
from mods import calc_functions
from fractions import Fraction
import numpy as np
from math import cos, sin, tan, acos, asin, atan
# import sympy as sym
# from sympy import *

#x, y = symbols("x y")

st.title('Calculus Functions')
st.header('Trig')
st.divider()

unit_circle = [0, 30, 45, 60, 90, 120, 135, 150, 180,
    210, 225, 240, 270, 300, 315, 330, 360]

radius = 1
pi = np.pi
ppi = 'π'
sqrrt = '√'
# st.write('pi:', pi)
e = 2.718281828459045
# st.write('e:', e)

def convert_to_symbols(num): 
    if num:
        # st.write('num: ', str(num))
        # st.write(f'type(num): {type(num)}')
        # st.write(f'not type(num) == str: {not type(num) == str}')
        # st.divider()
        if not isinstance(num, str):
            if num > 0.0:
                sign = ''
            else:
                sign = '-'
            # st.write(f'sign: {sign}')          
            if num == 0.0 or num == 1.0 or num == 2.0:
                result = str(num)
            elif str(round(abs(num), 5)) == str(round(sqrt(3), 5)):
                result = f'{sign}{sqrrt}3' 
            elif str(round(abs(num), 5)) == str(round(sqrt(3) / 3, 5)):
                result = f'{sign}{sqrrt}3/3'
            elif str(round(abs(num),5)) == str(round(2 * (sqrt(3) / 3),5)):
                result = f'{sign}2{sqrrt}3/3'
            elif str(round(abs(num), 6)) == str(round(sqrt(3) / 2, 6)):
                result = f'{sign}{sqrrt}3/2'
            elif str(round(abs(num), 6)) == str(round(sqrt(2) / 2, 6)):
                result = f'{sign}{sqrrt}2/2'
            elif str(round(abs(num), 5)) == str(round(sqrt(2), 5)):
                result = f'{sign}{sqrrt}2'
            elif str(abs(round(num, 1))) == '0.5':
                result = f'{sign}1/2'
            else:
                result = str(round(num, 6))
        else:
            result = num
        return str(result)
    
    
def calc_trig_function(num, denom):
    if not float(denom) == 0.0:
        result = float(num) / float(denom)
        
    else:
        result = 'undefined'
    return result


def create_rad_symbol(degrees):
    # Get the radians using pi symbol
    fraction = Fraction(degree , 180)
    if fraction.numerator == 1:            
        numerator = 'π'
    elif fraction.numerator == 0:                       
        numerator = 0
    elif degrees == 0.0 or degrees == 0:                       
        numerator = 0
    else:
        numerator = f'{fraction.numerator}π'
    if fraction.denominator == 1:
        separator, denominator = '', ''
    else:
        separator, denominator = '/', fraction.denominator
    radians = f'{numerator}{separator}{denominator}'
    return radians



def is_right_triangle(angle1, angle2, angle3):
    if angle1 == 90 or angle2 == 90 or angle3 == 90:
        return True
    else:
        return False

def sqrt(num):
    return np.sqrt(num)

        
# function to convert to superscript
def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)
  
# display superscipt
#st.write(get_super('GeeksforGeeks')) #ᴳᵉᵉᵏˢᶠᵒʳᴳᵉᵉᵏˢ
s2 = get_super('2')
s3 = get_super('3')
s4 = get_super('4')
s5 = get_super('5')


trig_funcs = {}
for degree in unit_circle:
    theta = np.deg2rad(degree)
    radians_pi = create_rad_symbol(degree)
    hyp = radius
    opp_angle = theta 
    right_angle = 90
    adj_angle = 90 - theta
    
         
    
    xcos = np.cos(theta)        
    ysin = np.sin(theta)
    if theta == 0.0:
        ysin = 0.0
        # x = xcos
        # y = ysin
    tan = calc_trig_function(ysin, xcos)
    sec = calc_trig_function(1, xcos) 
    csc = calc_trig_function(1, ysin)  # 1/sin or 1/y
    cot = calc_trig_function(1, tan)   # x/y or cos/sin
    
    new_angle = {
        'degrees': degree,
        'radians': radians_pi,
        'cos': xcos,
        'sin': ysin,
        'tan': tan,
        'sec': sec,
        'csc': csc,
        'cot': cot,
        'cos_sym': convert_to_symbols(xcos),
        'sin_sym': convert_to_symbols(ysin),
        'tan_sym': convert_to_symbols(tan),
        'sec_sym': convert_to_symbols(sec),
        'csc_sym': convert_to_symbols(csc),
        'cot_sym': convert_to_symbols(cot)
        } 
    
    trig_funcs[degree] = new_angle

for degree, angle_data in trig_funcs.items():
    pass    
    # st.write(f'{degree}')
    # st.write(f'{angle_data["radians"]}')
    # st.write(f'{angle_data["cos"]}')
    # st.write(f'Sine: {angle_data["sin"]}')
    # st.write(f'Tangent: {angle_data["tan"]}')
    # st.write(f'Secant: {angle_data["sec"]}')
    # st.write(f'Cosecant: {angle_data["csc"]}')
    # st.write(f'Cotangent: {angle_data["cot"]}')
    # st.write(f'Cosine Symbolic: {angle_data["cos_sym"]}')
    # st.write(f'Sine Symbolic: {angle_data["sin_sym"]}')
    # st.write(f'Tangent Symbolic: {angle_data["tan_sym"]}')
    # st.write(f'Secant Symbolic: {angle_data["sec_sym"]}')
    # st.write(f'Cosecant Symbolic: {angle_data["csc_sym"]}')
    # st.write(f'Cotangent Symbolic: {angle_data["cot_sym"]}')
    # st.write('-' * 40)
        

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
                if not tan == 'undefined':
                    #st.write(tan)
                    if tan == 0.0:
                        st.write(str(tan))
                    else:
                        st.write(convert_to_symbols(tan))
                else:
                    st.write(str(tan))
            # Cosecant
            with csc_col:
                if not csc == 'undefined':
                    st.write(convert_to_symbols(csc))
                else:
                    st.write(str(csc))      
            # Secant
            with sec_col:
                if not sec == 'undefined':
                    st.write(convert_to_symbols(sec))
                else:
                    st.write(str(sec))         
            # Cotangent
            with cot_col:
                if not cot == 'undefined':
                    st.write(convert_to_symbols(cot))
                else:
                    st.write(str(cot))
                
                
# arc_length = theta / radius        
# circumference = 2 * pi * radius
# area = pi * (radius ** 2)        
        
        
# Test the symbol conversion function        
# degrees = 30
# test_cos = cos(np.deg2rad(degrees))
# st.write(f'test_cos: {test_cos}')
# st.write(f'convert_to_symbols(test_cos): {convert_to_symbols(test_cos)}')

# test_angle = 30
# st.write(f'square root of 2 over 2: {np.sqrt(2)/2}')    
# test = get_sides_right(test_angle)
# st.write(f'test angle = {test_angle}, adj, opp sides: {str(test)}')
# st.divider()

# st.subheader(f'cos(90) == {(cos(pi/2))}')
# st.subheader(f'sin(90) == {(sin(pi/2))}')
# st.subheader(f'tan(90) == {(tan(pi/2))}')
# st.write(f'{sqrrt}3    == {sqrt(3)}')
# st.write(f'2{sqrrt}3/3 == {2 * sqrt(3) / 3}')
# st.write(f' {sqrrt}3/2 == {sqrt(3)/2}')
# st.write(f'{sqrrt}3/3  == {sqrt(3)/3}')
# st.write(f'{sqrrt}2    == {sqrt(2)}')
# st.write(f'{sqrrt}2/2  == {sqrt(2)/2} {sqrrt}2/2')


#st.write(f'a{s2} + b{s2} = c{s2}')

def get_sides_right(degrees):
    # How to calc x(adj) and y(opp) from angles and r(hyp)?
    # xcos = adj / hyp
    # a² + b² = c²
    # a² = c² - b²
    # a = √(c² - b²)
    # ((adj_ratio * hyp) ** 2) + ((opp_ratio * hyp) ** 2) = hyp ** 2
    # √a + √b = √c
    # adj + opp = hyp
    
    hyp = 1
    hyp_ratio = hyp / 90
    
    opp_angle = degrees
    hyp_angle = 90
    adj_angle = hyp_angle - opp_angle

    # Calculate the simplified ratios
    opp_ratio = opp_angle / hyp_angle
    adj_ratio = adj_angle / hyp_angle
    
    opp = sqrt(1 - (hyp * opp_ratio) ** 2)
    y = np.cos(degrees)    
    
    adj = (1 - (hyp * adj_ratio)) ** 2
    x = np.sin(degrees)
    
    st.write(f'adj_side: {adj}, sin({degrees}): {y})')
    st.write(f'opp_side: {opp}, cos({degrees}): {x})')
    opp = hyp * opp_ratio
    return adj, opp