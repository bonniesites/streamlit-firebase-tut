PAGE_HEADER = 'Scripture Text Search'
PAGE_SUBHEADER = 'Choose which Scriptures to Search'
SIDEBAR = 'collapsed'
# MENU_ITEMS = {
    # 'text': 'link'
# }

from mods.header import *
from mods.data_processing import *
# from mods.auth import *
from mods.utils import *
from mods.models import *


    
rootpath = 'pages/scriptures/'
#folderpath = '/Desktop/search_python/'
lds = 'lds-scriptures.txt'
bible = 'kjv-scriptures.txt'
quran = 'en.yusufali.txt'
my_label = "Choose Source to search:"
options = ("King James Bible", "All LDS Scriptures", "Quran")
MY_CHOICE = st.radio(label=my_label, options=options, horizontal=True)

# st.write('(LDS Scriptures contain: The King James version of The Holy Bible, The Book of Mormon: Another Testament of Jesus Christ, The Doctrine and Covenants, The Pearl of Great Price)')
submitted = False 
with st.form('scripture_search'):
    search_term = st.text_input('Enter search term:', value='', placeholder='Type search term here')
    submitted = st.form_submit_button('Search')
    
    if MY_CHOICE == 'King James Bible':
        file_path = rootpath + bible
        #st.success("file_path: " + file_path)
    elif MY_CHOICE == "All LDS Scriptures":
        file_path = rootpath + lds
    elif MY_CHOICE == "Quran":
        file_path = rootpath + quran
    else:
        st.warning('Please select one of the options.')
    if submitted:
        pattern = r'^[a-zA-Z0-9 ,.\-\']+$'
        if re.match(pattern, search_term): 
            search_file_name, search_count, search_lines = search_str(file_path, search_term, MY_CHOICE)      
    else:
        'Search term not valid, try again'

if submitted:
    left1, right1 = st.columns(2)
    with left1:            
        st.success(f'Results for "{search_term}": {search_count}') 
    with right1:     
        st.download_button(
            key='1',
            label="Download results", 
            file_name=search_file_name,
            data=search_file_name)

    for line in search_lines:           
        st.write(line, unsafe_allow_html=True)
                
    left, right = st.columns(2)
    with left:
        st.success(f'Results for "{search_term}": {search_count}')
    with right:                               
        st.download_button(
            key='2',
            label="Download results", 
            file_name=search_file_name,
                data=search_file_name)
    
    
st.divider()
st.link_button("Quran translation downloaded from Tanzil", "https://tanzil.net/trans/")

"For the Quran, the Abdullah Yusuf Ali version is used here."
