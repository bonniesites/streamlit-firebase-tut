from mods.base import *

radius = 1
pi = np.pi
ppi = 'π'
sqrrt = '√'
def set_italic(input):
    pass
    # return st.markdown(input, unsafe_allow_html=True)
sym_x = set_italic('x')
sym_y = set_italic('y')
sym_a = set_italic('a')
sym_c = set_italic('c')

# Euler's number
e = 2.718281828459045    

# expr = expr.replace('pi','π')

unit_circle = [0, 30, 45, 60, 90, 120, 135, 150, 180,
    210, 225, 240, 270, 300, 315, 330, 360]

calc_menu = [
  "AntiDerivative" #wk09
  , "Applied Optimization" #wk08
  , "Area" #wk09
  , "Chain Rule"  #wk04
  , "Concavity" #wk07
  , "Continuity" #wk03
  , "Definite Integrals" #wk10
  , "Derivatives" #wk04
  , "Differentiation" #wk04
  , "Exponents" #wk02
  , "Implicit" #wk05
  , "Improper Integrals" #wk13
  , "Indefinite Integrals" #wk11
  , "Integrals" #wk09
  , "Integration by Parts" #wk12
  , "Limits" #wk02
  , "Logarithms" #wk02
  , "Rate of Change" #wk06
  , "Mean Value Theorem" #wk07
  , "Second Derivative" #wk08
  , "Trig" #wk01
  , "U-Substitution" #wk10, 11
  , "Volume" #wk11, 12
]

calc_menu_left = [
  "AntiDerivative",
  "Applied Optimization",
  "Concavity",
  "Continuity",
  "Derivatives"]

calc_menu_mid = [
  "Differentiation",
  "Exponents",
  "Integrals",
  "Limits",
  "Logarithms"]

calc_menu_right = [
    "Rate of Change",
  "Theorems",
  "Trig",
  "U-Substitution",
  "Volume"]
    
    
def calc_trig_function(num, denom):
    if not float(denom) == 0.0 and not float(denom) == 0:
        result = float(num) / float(denom)        
    else:
        result = 'undefined'
    return result


def convert_to_symbols(num):
    if not isinstance(num, str):
        if num > 0.0:
            sign = ''
        else:
            sign = '-'         
        if abs(num) == 1.0:
            result = f'{sign}1'
        elif abs(num) == 2.0:
            result = f'{sign}2'
        elif num == 0.0 or num == 0:
            result = '0'
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


def create_rad_symbol(degrees):
    # Get the radians using pi symbol
    fraction = Fraction(degrees , 180)
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


def factor(product):
    f1 = 1
    f2 = product / f1
    factors = []
    while f1 < product:
        f1 += 1
        f2 = product / f1
        if not f1 in factors and product % f1 == 0:
            factors.append(f1)
    return factors




        
# function to convert to superscript
def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)
  
# display superscipt
#print(get_super('GeeksforGeeks')) #ᴳᵉᵉᵏˢᶠᵒʳᴳᵉᵉᵏˢ
sqrd = get_super('2')
cubd = get_super('3')
fourth = get_super('4')
fifth = get_super('5')

# lambda = '"\"{}'.format('u03BB')
# print('lambda: "\{}"'.format('u03BB'))
#sym.init_printing(use_unicode=False, wrap_line=True)

rad_angles = {
    '0':0, 
    'pi/6 or 30':pi/6, 
    'pi/4 or 45':pi/4, 
    'pi/3 or 60':pi/3, 
    'pi/2 or 90':pi/2, 
    '2*pi/3 or 120':2*pi/3, 
    '3*pi/4 or 135':3*pi/4, 
    '5pi/6 or 150':5*pi/6,
    'pi or 180':pi, 
    '7pi/6 or 210':7*pi/6, 
    '5pi/4 or 225':5*pi/4, 
    '4pi/3 or 240':4*pi/3, 
    '3pi/2 or 270':3*pi/2, 
    '5pi/3 or 300':5*pi/3, 
    '7pi/4 or 315':7*pi/4,
    '11pi/6 or 330':11*pi/6, 
    '2pi or 360':2*pi
    }

def calc_cfv(present, rate, time):
    fv = present * (e ** (rate * time))
    st.write(str(round(fv, 6)))


def is_polynomial(expression):
    # Remove whitespace and convert to lowercase for case-insensitive matching
    expression = expression.replace(" ", "").lower()
    
    # Define a regular expression pattern to match polynomial expressions
    pattern = r'^([+-]?(\d*x(\^\d+)?))+([+-]\d+)?$'
    
    # Use regex to match the pattern
    if re.match(pattern, expression):
        return True
    else:
        return False
    
def find_limit(eq_num, eq_denom, limit_num, x_given):
    if is_polynomial(eq_num) and is_polynomial(eq_denom):
        pass
    
def limit_table(eq_num, eq_denom, limit_num, x_given):
    left_limit, left_x, rt_limit, rt_x = st.columns(4)
    with left_limit:
        'Left X'
    with left_x:
        'Left f(x)'
    with rt_limit:
        'Right X'
    with rt_x:
        'Right f(x)'
    add_to = 1       
    for i in range(6):
        add_to  = add_to / 10        
        if limit_num < 0:
            limit_l = round(limit_num - add_to, 12) 
            limit_r = round(limit_num + add_to, 12)
        else:
            limit_l = round(limit_num * (-1) + add_to, 12) 
            limit_r = round(limit_num + add_to, 12)
        eq = f'{eq_num} / {eq_denom}'
        eq = eq.replace('^', str('**'))
        eq = eq.replace('sin x', str('np.sin(x)'))
        eq = eq.replace('cos x', str('np.cos(x)')) 
        eq = eq.replace('tan x', str('np.tan(x)'))   
        eq = eq.replace('csc x', str('1 / np.sin(x)'))
        eq = eq.replace('sec x', str('1 / np.cos(x)')) 
        eq = eq.replace('cot x', str('1 / np.tan(x)'))  
        eq = eq.replace('sqrt', str('np.sqrt')) 
        eq_l = eq.replace('x', f'{limit_l}')
        eq_r = eq.replace('x', f'{limit_r}')        
        x_val_l = round(eval(eq_l), 12)
        x_val_r = round(eval(eq_r), 12)        
        # st.subheader(eq)  
        with left_limit:
            st.write(str(limit_l))
        with left_x:
            st.write(str(x_val_l))
        with rt_limit:
            st.write(str(limit_r))
        with rt_x:
            st.write(str(x_val_r))
    
def regex_matches(pattern, expr):
    if not re.match(pattern, expr):
        st.warning('Invalid characters found:', re.sub(pattern, '', expr))
        st.write('Please try again.')
        return False
    else:
        #st.write('Expression is valid.')
        return True
            