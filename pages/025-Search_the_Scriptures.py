PAGE_HEADER = 'Scripture Text Search'
PAGE_SUBHEADER = 'Choose which Scriptures to Search'
SIDEBAR = 'collapsed'
# MENU_ITEMS = {
    # 'text': 'link'
# }

from mods.base import *
from mods.utils import *

# Initialization
if 'count' not in st.session_state:
    st.session_state.count = ''
if 'results' not in st.session_state:
    st.session_state.results = ''
    
rootpath = 'pages/scriptures/'
#folderpath = '/Desktop/search_python/'
lds = 'lds-scriptures.txt'
bible = 'kjv-scriptures.txt'
quran = 'en.yusufali.txt'
my_label = "Choose Source to search:"
options = ("King James Bible", "All LDS Scriptures", "Quran")
my_choice = st.radio(label=my_label, options=options, horizontal=True)

# st.write('(LDS Scriptures contain: The King James version of The Holy Bible, The Book of Mormon: Another Testament of Jesus Christ, The Doctrine and Covenants, The Pearl of Great Price)')
    
with st.form('scripture_search'):
    search_term = st.text_input('Enter search term:', value='', placeholder='Type search term here')
    #search_term = r'\b' + re.escape(raw_search) + r'\b'
    #raw_search
    #search_term
    submitted = st.form_submit_button('Search')
    if my_choice == 'King James Bible':
        file_path = rootpath + bible
    elif my_choice == "All LDS Scriptures":
        file_path = rootpath + lds
    elif my_choice == "Quran":
        file_path = rootpath + quran
    else:
        st.warning('Please select one of the options.')
if submitted:
    pattern = r'^[a-zA-Z0-9 ,.\-\']+$'
    if re.match(pattern, search_term):
        search_term
        search_results = search_str(file_path, search_term)
        search_results
        left, right = st.columns(2)
        with left:
            count_box = st.empty()
        with right:
            download_box = st.empty()            
        with left:
            with count_box:
                lines = read_file(results)
                for line in lines:
                    st.write(line)
        with right:            
            with download_box:
                file_name = f'{search_term}.txt'
                st.download_button(
                    label="Download results", 
                    file_name=file_name,
                    data=file_name)    
    else:
        'Search term not valid, try again'
    
st.divider()
st.link_button("Quran translation downloaded from Tanzil", "https://tanzil.net/trans/")

"For the Quran, the Abdullah Yusuf Ali version is used here."
