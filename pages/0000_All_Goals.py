from mods.db import *

if 'filter_choice' not in st.session_state:
    st.session_state.filter_choice = 'All' 
    
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = ''

print('inside All_Goals.import mods.db')
# import pyautogui


PAGE_HEADER = 'All Goals, Searchable, Filter Options'
PAGE_SUBHEADER = st.session_state.filter_choice

ALL_GOALS_LIST = list(ALL_GOALS_CURSOR)

print('inside All_Goals page')

#display_message(f'Screen size: {pyautogui.size()}, \n\n Mouse position: {pyautogui.position()}', .5)

# Check Streamlit version for compatibility
#print(f"Streamlit version: {st.__version__}")

# custom_print("Session State Variables:")
# for key, value in st.session_state.items():
#     custom_print(f"{key}: {value}")

# TODO: set up pydantic model for categories and link to goals

COUNTER = 0

#############
# Functions #
#############

def list_goals():
    custom_print('inside All_Goals.list_goals()')
    for goal in ALL_GOALS:
        # Display fields of the current document
        fields = ''
        for key, value in goal.items():
            fields += f'\n\n{value} ||  '
        st.warning(fields)
 
def add_test_goals():
    custom_print('inside All_Goals.add_test_goals()')
    #display_message(f'str(GOALS_LIST): {str(GOALS_LIST)}')
    if ALL_GOALS is not None:
        #display_message('Adding test goals')
        for goal in test_data:
            newgoal = {
                'timestamp' : datetime.now(), 
                'category' : goal[1], 
                'goal_task' : goal[2], 
                'duedate' : datetime.now() + timedelta(days=3), 
                'is_done' : goal[0] 
            }
            #logging.debug(f"New goal document: {newgoal}")
            #display_message('Adding test goals', .5)
            check_exists = check_existing_doc(GOALS_LIST, newgoal)
            if check_exists:
                add_new_document(GOALS_LIST, newgoal)

def main():
    custom_print('inside All_Goals.main)')
    #st.sidebar.write('start main()')
    with st.sidebar:
        custom_print('inside All_Goals.sidebar')
    # with search:       
        # box, btn = st.columns(2)
        # with box:
        with st.form('search_form'):
            custom_print('inside All_Goals.search_form')
            search_terms = st.text_input('Search goals:')
            # with btn:
            submitted = st.form_submit_button('Search', help='Search in goals', type='primary')
        if submitted:
            custom_print('inside All_Goals.submitted search_form')
            if st.button('Clear search', type='secondary'):
                st.session_state.search_terms = ''
            st.session_state.search_terms = search_terms
            #st.rerun()
    
        filter_choice = st.sidebar.selectbox("Filter by:", ['All', 'Done', 'Pending'])
        custom_print(f'filter_choice: {filter_choice}')
        if filter_choice:
            st.session_state.filter_choice = filter_choice
        
        
        filter_option = query_list(st.session_state.filter_choice, st.session_state.search_terms)
            
# with sort:
#     with st.form('sort_form'):
#         sort_term = st.text_input('Sort')
#         submitted = st.form_submit_button('Sort', type='primary', help='Sort in goals')
#         if submitted:
#             sort_results = sort_documents(GOALS_LIST, sort_term)
#             if sort_results:
#                 custom_print('Sort results:')
#                 for result in sort_results:
#                     custom_print(result)
#             else:
#                 custom_print('No sort results found.')
    
    if st.session_state.user_role == 'admin':
        st.divider()
        col_del, col_add_test = st.columns(2)
        with col_del:
            # Debug button to delete all goals
            if st.button("Delete all goals", key="delete_all_docs", type='secondary'):
                display_message('Deleting all goals')
                delete_all_documents(GOALS_LIST)
        with col_add_test:
            if st.button("Add test data", key="add_test_data", type='primary'):
                add_test_goals()

title, btn, btn2 = st.columns(3)
with title:
    st.subheader(f'My SMART Goals Journal - {PAGE_SUBHEADER}')
with btn:
    add_goal()
with btn2:
    refresh_goals(ALL_GOALS_LIST)


search_terms = ''
#filter_query = query_coll(st.session_state['filter_choice'], st.session_state.search_terms)
filter_query = query_list(ALL_GOALS_COLL,'All', search_terms)

#st.sidebar.write(f'st.session_state.sort: {st.session_state.sort}')
#st.sidebar.write(f'st.session_state.sort_order: {st.session_state.sort_order}')
#goal_list = GOALS_LIST.find(filter_query).sort(st.session_state.sort, st.session_state.sort_order)

#goal_list = GOALS_LIST.find(filter_query).sort([('timestamp', -1)])  
#goal_list = GOALS_LIST.find(filter_query)
#goal_list.sort(key=lambda x: x.get('timestamp', 0), reverse=True)


GOALS_DB = CLIENT.goals
ALL_GOALS_COLL = GOALS_DB.goals_list
ALL_GOALS_CURSOR = ALL_GOALS_COLL.find()
ALL_GOALS_LIST = list(ALL_GOALS_CURSOR)

#print(f'line 168 ALL_GOALS_COLL: \n {ALL_GOALS_COLL}')
#print(f'ALL_GOALS_CURSOR: \n {ALL_GOALS_CURSOR}')
#print(f'ALL_GOALS_LIST: \n {ALL_GOALS_LIST}')
COLL_count = ALL_GOALS_COLL.count_documents({})
#print(f"Number of documents in ALL_GOALS_COLL: {COLL_count}")
cursor_count = len(ALL_GOALS_LIST)
#print(f"Number of documents in ALL_GOALS_CURSOR: {cursor_count}")


#goal_list = list(goal_list)    
col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1, 2, 3, 2, 2])
with col_markdone:
    ''
with col_edit:
    ''
with col_delgoal:
    ''
with col_cat:
    # Button to sort goals by category using session variables to hold sort_column and asc/desc
    st.button('Category', 'sort_record_list(ALL_GOALS_LIST, "category")')
with col_goal:
    'Goal Task'
with col_due:
    'Due Date'
with col_timestamp:
    'Set Date'
render_goals(ALL_GOALS_LIST)

if __name__ == "__main__":
    main()

