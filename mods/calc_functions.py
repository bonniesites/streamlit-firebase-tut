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
  "AntiDerivative",
  "Applied Optimization",
  "Concavity",
  "Continuity",
  "Derivatives",
  "Differentiation",
  "Exponents",
  "Integrals",
  "Limits",
  "Logarithms",
  "Rate of Change",
  "Theorems",
  "Trig",
  "U-Substitution",
  "Volume"
]

calc_menu_left = [
  "AntiDerivative",
  "Applied Optimization",
  "Concavity",
  "Continuity"
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