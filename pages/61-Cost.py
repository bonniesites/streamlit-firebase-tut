PAGE_TITLE = 'Soaping'
PAGE_SUBHEADER = 'Cost Calculator'
SIDEBAR = 'collapsed'
PAGE_LAYOUT = 'wide'
MENU_ITEMS = {
       'SAP Calculator': '/SAP',
       'Cost Calculator': '/Cost'
}

from mods.base import *

OZ_PER_LB = 16


#leftcol, midcol, rightcol = st.columns(3)


with st.expander('Add a Vendor'):        
    # Create form for to save data entry to DB  TODO: Use AI to look it up from link
    call_back = None
    button_text = 'Add Vendor'
    form_name = 'vendor_form'       
    # create_form(vendor_inputs, button_text, form_name, True, call_back=call_back)
    # form_inputs_name = f'{form_name}_inputs'       
    # if st.session_state[form_inputs_name]:
    #     utils.save_record(st.session_state[form_inputs_name], form_name)
st.divider()
    
# with midcol:
#     st.write('')
    # Get data from DB using query on search term
    # Buttons to choose to Search by product, vendor, productID 
    # for item in soap_search:
    #     link = 'item'
    #     link_text = item.replace('_', ' ')
    #     create_button(link, link_text)
        
    # Calculate cost/unit, display cost per unit/ vendors/sizes/total cost/total units/link
    
prod_cost_list = {
    'vendor': 'Amazon'
    , 'product': 'Lye'
    , 'unit_name': 'lbs'
    , 'units': 2
    , 'oz': 4 * 16
    , 'cost': ''
    , '': ''
    , '': ''
    , '': ''
    , '': ''
    , '': ''
    , '': ''
}
    
# TODO: Get query data from DB

prod_name, lbs, oz, cost, unit_cost, link_col = st.columns(6)
with prod_name:
    'Product'
    'Lye-NaOH'
    'Lye-KOH'
    'Coconut oil-gallon'
    'Coconut oil-pail'
    'Castor oil-gallon'
    'Neem oil-gallon'
    'Cocoa Butter-cube'
    'Mango Butter-cube'
    'Canola oil-gallon'
    'Canola oil-cube'
with lbs:
    'Lbs'
    '4'
    '4'
    '7'
    '44'
    '7'
    '7'
    '10'
    '10'
    '7'
    '35'
with oz:
    'Ounces' 
    st.write(f'{4 * OZ_PER_LB}') 
    st.write(f'{4 * OZ_PER_LB}')  
    st.write(f'{7 * OZ_PER_LB}') 
    st.write(f'{44 * OZ_PER_LB}') 
    st.write(f'{7 * OZ_PER_LB}') 
    st.write(f'{7 * OZ_PER_LB}') 
    st.write(f'{10 * OZ_PER_LB}') 
    st.write(f'{10* OZ_PER_LB}') 
    st.write(f'{7* OZ_PER_LB}') 
    st.write(f'{35* OZ_PER_LB}')
with cost:
    'Total Cost'
    '27.15'
    '27.75'
    '12.32'
    '60.00'
    '16.50'
    '53.68'
    '47.86'
    '55.30'
    '9l.23'
    '67.50'
with unit_cost:
    'Unit cost'
    st.write(f'${round(27.15 / (4 * OZ_PER_LB), 2)}')    
    st.write(f'${round(27.75 / (4 * OZ_PER_LB), 2)}')
    st.write(f'${round(12.32 / (7 * OZ_PER_LB), 2)}')
    st.write(f'${round(60.00 / (44 * OZ_PER_LB), 2)}')
    st.write(f'${round(16.50 / (7 * OZ_PER_LB), 2)}')
    st.write(f'${round(53.68 / (7 * OZ_PER_LB), 2)}')
    st.write(f'${round(47.86 / (10 * OZ_PER_LB), 2)}')
    st.write(f'${round(55.30 / (10 * OZ_PER_LB), 2)}')
    st.write(f'${round(9.23 / (7 * OZ_PER_LB), 2)}')
    st.write(f'${round(67.50 / (35 * OZ_PER_LB), 2)}')
with link_col:
    'Product link'
    create_button('https://www.amazon.com/gp/product/B09L5D8B2W/ref=ox_sc_saved_title_7?smid=A1M4G5OUETNA4Z&psc=1', 'Amazon')
    create_button('https://www.soaperschoice.com/coconut-76-55007sc?returnurl=%2fbase-oils%2f', 'Soapers Choice')
    create_button('https://www.soaperschoice.com/coconut-76-55044sc?returnurl=%2fbase-oils%2f', 'Soapers Choice')
    create_button('https://www.soaperschoice.com/castor-oil-usp-91507sc?returnurl=%2fbase-oils%2f', 'Soapers Choice')
    create_button('https://www.soaperschoice.com/neem-oil-conventional-86307sc?returnurl=%2fsearch%3fq%3dneem', 'Soapers Choice')
    create_button('https://www.soaperschoice.com/cocoa-butter-prime-pressed-59010sc?returnurl=%2fsearch%3fq%3dcocoa%2bbutter', 'Soapers Choice')
    create_button('https://www.soaperschoice.com/mango-butter-89010sc?returnurl=%2fsearch%3fq%3dmango%2bbutter', 'Soapers Choice')
    create_button('https://www.soaperschoice.com/canola-salad-50036sc?returnurl=%2fsearch%3fq%3dcanola', 'Walmart')
    create_button('https://www.soaperschoice.com/canola-salad-50036sc?returnurl=%2fsearch%3fq%3dcanola', 'Soapers Choice')
    create_button('https://www.amazon.com/Potassium-Hydroxide-Grade-Caustic-Potash/dp/B0C15B9NK1/ref=pd_bxgy_img_sccl_1/135-3681823-2865364?pd_rd_w=ODp0j&content-id=amzn1.sym.7746dde5-5539-43d2-b75f-28935d70f100&pf_rd_p=7746dde5-5539-43d2-b75f-28935d70f100&pf_rd_r=CKEHRB7B1G87QNZ6WNYV&pd_rd_wg=rK41g&pd_rd_r=3b773a9f-fc57-40e8-845e-95182c4dd8c6&pd_rd_i=B0C15B9NK1&psc=1', 'Amazon')
        
        
        
        
        
        
    # for item in calc_menu_right:
    #     link = item
    #     link_text = item.replace('_', ' ')
    #     utils.create_button(link, link_text)



