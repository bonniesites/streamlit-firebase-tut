PAGE_HEADER = 'Scripture Text Search'
PAGE_SUBHEADER = 'Choose which Scriptures to Search'
SIDEBAR = 'collapsed'
# MENU_ITEMS = {
    # 'text': 'link'
# }

from mods.base import *

# Initialization
if 'count' not in st.session_state:
    st.session_state.count = ''
if 'results' not in st.session_state:
    st.session_state.results = ''
    
rootpath = 'pages/scriptures/'
#folderpath = '/Desktop/search_python/'
lds_scriptures = 'lds-scriptures.txt'
bible_file = 'kjv-scriptures.txt'

my_label = "Choose Source to search:"
options = ("Bible only", "All LDS Scriptures")
my_choice = st.selectbox(label=my_label, options=options, index=None)
# st.write('If Bible only is toggled off, all LDS Scriptures will be searched:')
# st.write('(KJV Bible, Book of Mormon, Doctrine and Covenants, Pearl of Great Price)')
    
with st.form('scripture_search'):
    search_term = st.text_input('Enter search term:', value='', placeholder='Enter term here')
    submitted = st.form_submit_button('Search')
if my_choice == 'Bible only':
    file_path = rootpath + bible_file
elif my_choice == "All LDS Scriptures":
    file_path = rootpath + lds_scriptures
else:
    st.error('Please select one of the options.')
if submitted:
    pattern = '^[a-zA-Z0-9]+$'
    if regex_matches(pattern, search_term):
        results = search_str(file_path, search_term)
        st.session_state.count = results[1]
        if not results[0] == '':
            st.session_state.results = results[0]
        else:
            st.warning('Search term not found!')
        file_name = f'{search_term}.txt'






# Get file
# search_str(filepath, textstring)
# search_str(biblepath, textstring)
# search_str(filepath, textstring)


