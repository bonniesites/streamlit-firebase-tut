from datetime import datetime, timedelta
import streamlit as st

from mods.db import *

PAGE_HEADER = 'Achieved Goals, Searchable, Filter Options'
PAGE_SUBHEADER = 'Achieved'
# import pyautogui

#display_message(f'Screen size: {pyautogui.size()}, \n\n Mouse position: {pyautogui.position()}', .5)

# TODO: set up pydantic model for categories and link to goals
CATEGORIES = ALL_GOALS_CURSOR.distinct("category")
counter_box = st.sidebar.empty()

if 'popover' not in st.session_state:
       st.session_state.popover = True

if 'filter_choice' not in st.session_state:
       st.session_state.filter_choice = 'Done'

if 'search_terms' not in st.session_state:
    st.session_state.search_terms = '' 

if 'filter_option' not in st.session_state:
    st.session_state.filter_option = {'is_done': True} 
else:
    st.session_state.filter_option = {'is_done': True} 

if 'srt_by' not in st.session_state:
    st.session_state.sort = 'timestamp' 
    
if 'srt_order' not in st.session_state:
    st.session_state.srt_order = -1
    
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'guest'

# # Get Streamlit version
# streamlit_version = st.__version__
# Display Streamlit version in your app
# st.header(f"Streamlit version: {streamlit_version}")



            
FILTERED_DONE_GOALS_CURSOR = query_list(ALL_GOALS_COLL, st.session_state.filter_option, st.session_state.search_terms)
#print(f' \n FILTERED_DONE_GOALS_CURSOR: {FILTERED_DONE_GOALS_CURSOR}')

FILTERED_DONE_GOALS_LIST = list(FILTERED_DONE_GOALS_CURSOR)
# for goal in FILTERED_DONE_GOALS_LIST:
        # custom_print(f'goal: {goal}')     
COUNTER = 1


#############
# Functions #
#############

def list_goals():
    for goal in DONE_GOALS_CURSOR:
        # Display fields of the current document
        fields = ''
        for key, value in goal.items():
            fields += f'\n\n{value} ||  '
        st.warning(fields)
 
def add_test_goals():
    custom_print('invoked Done.add_test_goals()')
    display_message(f'str(GOALS_LIST): {str(GOALS_LIST)}')
    if DONE_GOALS_CURSOR is not None:
        display_message('Adding test goals')
        for goal in test_data:
            for key, value in goal.items():
                custom_print(f"Key: {key}, Value: {value}")
            newgoal = {
                'timestamp' : datetime.now(), 
                'category' : goal[1], 
                'goal_task' : goal[2], 
                'duedate' : datetime.now() + timedelta(days=3), 
                'is_done' : goal[0] 
            }
            #logging.debug(f"New goal document: {newgoal}")
            display_message('Adding test goals', .5)
            check_exists = check_existing_doc(GOALS_LIST, newgoal)
            if check_exists:
                add_new_document(GOALS_LIST, newgoal)

# # Format the goal text based on is_done value
# def format_goal_text(document):
#     fields = ''         
#     # Use the function to format the goal text
#     for field in document:
#         fields += f'field: {field}\n'
#     if document['is_done']:
#         return f"<del>{document['goal_task']}</del>"
#     else:
#         return document['goal_task']



# def query_coll(filter_option, search_terms):
#     #st.write('Setting up filter options...')
#     # Set query to exclude the option keys
#     query = {"category": {"$not": {"$regex": "option"}}}    
#     if filter_option.lower() == 'done':
#         query['is_done'] = True
#     elif filter_option.lower() == 'pending':
#         query['is_done'] = False
#     elif filter_option.lower() != 'all':
#         raise ValueError("Invalid filter option")
        
#     # if 'is_done' in query:  # Check if 'is_done' key is present in the query
#     #     st.write(f"query['is_done']: {query['is_done']}")    
#     if search_terms:
#         search_query = {
#             "$or": [
#                 {"category": {"$regex": search_terms, "$options": "i"}},
#                 {"goals_task": {"$regex": search_terms, "$options": "i"}}
#             ]
#         }
#         # Combine search query with existing query using "$and"
#         query = {"$and": [query, search_query]}    
#     #st.write(f'query: {query}')  # Check the final query    
#     return query


def main():
    custom_print('invoked Done.main()')
    #st.sidebar.write('start main()')
    with st.sidebar:
        with st.form('search_form'):
            search_terms = st.text_input('Search goals:')
            submitted = st.form_submit_button('Search', type='primary', help='Search in goals')
        if submitted:
            if st.button('Clear search', type='secondary'):
                st.session_state.search_terms = ''
            st.session_state.search_terms = search_terms
            #st.rerun()
            # TODO: filter by keyword in column or goal task text
            # TODO: fix sort   
             
    # with sort:
    #     with st.form('sort_form'):
    #         sort_term = st.text_input('Sort')
    #         submitted = st.form_submit_button('Sort', type='primary', help='Sort in goals')
    #         if submitted:
    #             sort_results = sort_documents(GOALS_LIST, sort_term)
    #             if sort_results:
    #                 st.write('Sort results:')
    #                 for result in sort_results:
    #                     st.write(result)
    #             else:
    #                 st.write('No sort results found.')
        
        # if st.session_state.user_role == 'admin':
        #     st.divider()
        #     col_del, col_add_test = st.columns(2)
        #     with col_del:
        #         # Debug button to delete all goals
        #         if st.button("Delete all goals", key="delete_all_docs", type='secondary'):
        #             display_message('Deleting all goals')
        #             delete_all_documents(GOALS_LIST)
        #     with col_add_test:
        #         if st.button("Add test data", key="add_test_data", type='primary'):
        #             add_test_goals()

    title, btn = st.columns(2)
    with title:
        st.subheader(F'My {PAGE_SUBHEADER} SMART Goals!')
    with btn:
        add_goal()
        
    
    
    st.sidebar.write(f'st.session_state.sort: {st.session_state.sort}')
    st.sidebar.write(f'st.session_state.srt_order: {st.session_state.srt_order}')
    goal_list = ALL_GOALS_COLL.find({'is_done': True}).sort('timestamp', 1) 
    goal_list = list(goal_list)   
    col_count, col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1, 1, 2, 2, 2, 2])
    with col_count:
        'Count'
    with col_markdone:
        ''
    with col_edit:
        ''
    with col_delgoal:
        ''
    with col_cat:
        # Button to sort goals by category using session variables to hold sort_column and asc/desc
        st.button('Category', change_sort_order())
    with col_goal:
        'Goal Task'
    with col_due:
        'Due Date'
    with col_timestamp:
        'Set Date'
    render_goals(FILTERED_DONE_GOALS_LIST)

if __name__ == "__main__":
    main()