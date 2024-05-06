import streamlit as st
# TODO: Hide menu until logged in/authenticated, then show menu
    

css = '''
<style>
       .reportview-container 
       {
            margin-top: -2em;
        }
       #stDecoration, .stDeployButton
       {
        min-width: 0px;
        max-width: 350px;
        display: none important!;
        visibility: hidden important!;
       }
</style>
'''

# st.markdown("""
#     <style>
#         .reportview-container {
#             margin-top: -2em;
#         }
#         #MainMenu {visibility: hidden;}
#         .stDeployButton {display:none;}
#         footer {visibility: hidden;}
#         #stDecoration {display:none;}
#     </style>
# """, unsafe_allow_html=True)

st.markdown(css, unsafe_allow_html=True)

## This goes in the custom format as a new line after debugging: 
## footer {visibility: hidden;}
custom_format = '''
       <style>
       #root {background-image: url('https://images.unsplash.com/photo-1688453756951-842a78eec6ad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2535&q=80');
       background-size: cover;}
       </style>
       '''
st.markdown(custom_format, unsafe_allow_html=True)

# Global variables

goal_form_inputs = {
       'goal_title':{'type':'text', 'label':'Goal text', 'required':True, 'pattern':''},
       'goal_done':{'type':'toggle', 'label':'Goal Done'},
       'goal_url':{'type':'text', 'label':'Link URL'},
       'goal_image':{'type':'upload', 'label':'Choose icon'},
       'goal_cat':{'type':'text', 'label':'Goal category'},
       'goal_due_date':{'type':'date', 'label':'Due Date'}
}

post_form_inputs = {
       'post_title':{'type':'text', 'label':'Post title'},
       'post_content':{'type':'textarea', 'label':'Post content'},
       'post_url':{'type':'text', 'label':'Link URL'},
       'post_image':{'type':'text', 'label':'Image location'},
       'post_cat':{'type':'select', 'label':'Post category'}
}

user_form_inputs = {
       'username':{'type':'text', 'label':'Username', 'required':True,
        'pattern':''},
       'first':{'type':'text','label':'First name'},
       'last':{'type':'text','label':'Last name'},
       'email':{'type':'text','label':'Email'},
       'street_address':{'type':'text','label':'Street address'},
       'postal_code':{'type':'text','label':'Postal/zip code'},
       'phone':{'type':'text','label':'Phone number'},
       'month':{'type':'text','label':'Birthday month'},
       'day':{'type':'text','label':'Birthday day'},
       'avatar':{'type':'image','label':'Avatar'}
}

# cfv_form_inputs = [
#        'present':'Present value'
#        ,'rate': 'Interest Rate'
#        ,'time': 'Time'
#        #,'period': 'Period'
# ]


# vendor_form_inputs = [
#        'company': 'Company name',
#        'contact_first': 'First name',
#        'contact_last': 'Last name',
#        'email': 'Email',
#        'street_address': 'Street address',
#        'postal_code': 'Postal/zip code',
#        'phone': 'Phone number',
#        'url': 'Website URL address',
#        'day': 'Birthday day',
#        'avatar': 'Logo'
# ]

# cost_form_inputs = [
#        'vendorID': 'Vendor', # use select drawing from vendors collection, also have Add New button
#        'product': 'Product',  # use select from products collection, also have Add New button
#        'unit_name': 'Unit name',
#        'units': 'Number of units', # use slider?
#        'street_address': 'Street address',
#        'postal_code': 'Postal/zip code',
#        'phone': 'Phone number',
#        'month': 'Birthday month',
#        'day': 'Birthday day',
#        'avatar': 'Avatar'
# ]

