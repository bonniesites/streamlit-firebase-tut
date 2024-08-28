from mods.db import *

PAGE_HEADER = 'All Goals, Searchable, Filter Options'
PAGE_SUBHEADER = 'Pending'

PENDING_GOALS_LIST = list(PENDING_GOALS_CURSOR)
# for goal in PENDING_GOALS_LIST:
#     custom_print(f' \n goal: {goal} \n ')

if 'search_terms' not in st.session_state:
    # st.write("search_terms not found in session_state. Initializing...")
    st.session_state.search_terms = ''    
    # st.write("Current search_terms: ", st.session_state.search_terms)
# else:    
    # st.write("Current search_terms: ", st.session_state.search_terms)

if 'filter_choice' not in st.session_state:
    st.session_state.filter_choice = 'Pending'

if 'srt_by' not in st.session_state:
    st.session_state.srt_by = 'timestamp' 
    
if 'srt_ord' not in st.session_state:
    st.session_state.srt_ord = pymongo.DESCENDING
    
if 'user_role' not in st.session_state:
    st.session_state.user_role = ''

def main():
    #st.sidebar.write('start main()')

    with st.sidebar:
    # with search:       
        # box, btn = st.columns(2)
        # with box:
        with st.form('search_form'):
            st.session_state.search_terms = st.text_input('Search goals:')
            submitted = st.form_submit_button('Search', type='primary', help='Search in goals')
        if submitted:
            if st.button('Clear search', type='secondary'):
                st.session_state.search_terms = ''
            st.write(f'st.session_state.search_terms: {st.session_state.search_terms}')
            st.write(f'st.session_state.filter_choice: {st.session_state.filter_choice}')
            filter_choice = query_coll(st.session_state.filter_choice, st.session_state.search_terms)
            FILTERED_DONE_GOALS_CURSOR = list(filter_choice)
        
        if st.session_state.user_role == 'admin':
            st.divider()
            col_del, col_add_test = st.columns(2, gap='small')
            with col_del:
                # Debug button to delete all goals
                if st.button("Delete all goals", key="delete_all_docs", type='secondary'):
                    display_message('Deleting all goals')
                    delete_all_documents(GOALS_LIST)
            with col_add_test:
                if st.button("Add test data", key="add_test_data", type='primary'):
                    add_test_goals()

    title, btn = st.columns([5, 3], gap='small')
    with title:
        st.subheader(f'My {PAGE_SUBHEADER} SMART Goals Journal')
    with btn:
        add_goal()

            
    FILTERED_PENDING_GOALS_CURSOR = query_list(ALL_GOALS_COLL, st.session_state.search_terms, st.session_state.filter_choice)
    #print(f' \n FILTERED_PENDING_GOALS_CURSOR: {FILTERED_PENDING_GOALS_CURSOR}')

    FILTERED_PENDING_GOALS_LIST = list(FILTERED_PENDING_GOALS_CURSOR)
    # for goal in FILTERED_PENDING_GOALS_LIST:
          # custom_print(f'goal: {goal}')     
       
    
    
    render_goals(FILTERED_PENDING_GOALS_LIST)

if __name__ == "__main__":
    main()