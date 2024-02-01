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
lds = 'lds-scriptures.txt'
bible = 'kjv-scriptures.txt'

my_label = "Choose Source to search:"
options = ("King James Bible", "All LDS Scriptures")
my_choice = st.radio(label=my_label, options=options, horizontal=True)
# st.write('If Bible only is toggled off, all LDS Scriptures will be searched:')
# st.write('(KJV Bible, Book of Mormon, Doctrine and Covenants, Pearl of Great Price)')
    
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
    else:
        st.warning('Please select one of the options.')
if submitted:
    pattern = r'^[a-zA-Z0-9 ,.\-\']+$'
    if regex_matches(pattern, search_term):
        results = find_similar_fuzzy_in_file(search_term, file_path)
        #st.session_state.count = results
        #st.session_state.count
        if not results:
            st.session_state.results = results
            st.session_state.results
        else:
            st.warning('Search term not found!')
        file_name = f'{search_term}.txt'
    else:
        'Search term not valid, try again'

# # Example usage
# text = "This is a sample text. It contains words like sample, example, and simple."
# search_term = "sample"
# matches = find_similar_fuzzy(search_term, text)

# matches


# Get file
# search_str(filepath, textstring)
# search_str(biblepath, textstring)
# search_str(filepath, textstring)


