PAGE_HEADER = 'ACCOMPLISHED Goals, Searchable, Filter Options'
PAGE_SUBHEADER = 'ACCOMPLISHED'

from mods.header import *
# from mods.models import *
from mods.data_processing import *
# from mods.utils import *

# import pyautogui

#display_message(f'Screen size: {pyautogui.size()}, \n\n Mouse position: {pyautogui.position()}', .5)

# TODO: set up pydantic model for categories and link to goals
CATEGORIES = ALL_GOALS.distinct("category")
counter_box = st.sidebar.empty()

# # Get Streamlit version
# streamlit_version = st.__version__
# Display Streamlit version in your app
# st.header(f"Streamlit version: {streamlit_version}")

# Iterate over each document and display its fields
DONE_GOALS = list(DONE_GOALS)
print(DONE_GOALS)
# COUNTER variable for keys
COUNTER = 1

if 'popover' not in st.session_state:
       st.session_state.popover = True

if 'search_term' not in st.session_state:
    # st.write("search_term not found in session_state. Initializing...")
    st.session_state.search_term = 'goals'    
    # st.write("Current search_term: ", st.session_state.search_term)
# else:    
    # st.write("Current search_term: ", st.session_state.search_term)

if 'filter_option' not in st.session_state:
    st.session_state.filter_option = {'is_done': True} 
else:
    st.session_state.filter_option = {'is_done': True} 

if 'sort' not in st.session_state:
    st.session_state.sort = 'timestamp' 
    
if 'srt_order' not in st.session_state:
    st.session_state.srt_order = pymongo.DESCENDING
    
if 'user_role' not in st.session_state:
    st.session_state.user_role = ''


#############
# Functions #
#############

def list_goals():
    for goal in DONE_GOALS:
        # Display fields of the current document
        fields = ''
        for key, value in goal.items():
            fields += f'\n\n{value} ||  '
        st.warning(fields)
 
def add_test_goals():
    display_message(f'str(GOALS_LIST): {str(GOALS_LIST)}')
    if DONE_GOALS is not None:
        display_message('Adding test goals')
        for goal in test_data:
            for key, value in goal.items():
                print(f"Key: {key}, Value: {value}")
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

# Format the goal text based on is_done value
def format_goal_text(document):
    fields = ''         
    # Use the function to format the goal text
    for field in document:
        fields += f'field: {field}\n'
    if document['is_done']:
        return f"<del>{document['goal_task']}</del>"
    else:
        return document['goal_task']

def render_goal(document, is_journal):
    global COUNTER
    # Create separate columns for each field and button
    col_count, col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1.25, 1, 2.5, 3, 2, 2], gap='small')
    with col_count:
        st.write(COUNTER)
        COUNTER += 1
    counter_box.write(f'counter_box Goal count = {COUNTER}')
    # Add buttons for editing, deleting, and marking as done
    with col_markdone:
        #st.write(document)
        if 'is_done' in document and document['is_done']:
            icon = ':leftwards_arrow_with_hook:'
            help_text = 'Undo goal achievement'
        else:
            icon = ':white_check_mark:'
            help_text = "Mark the goal as achieved"
        if st.button(icon, key=f"mark_done_{document['_id']}", help=help_text, use_container_width=False):
            # Toggle mark as done
            toggle_bool(GOALS_LIST, document['_id'],'is_done')
            #toggle_mark_as_done(GOALS_LIST, document['_id'])
            st.balloons()
            st.rerun()  # Rerun the app to reflect changes
    with col_edit:
        if st.session_state.popover:
            with st.popover(":pencil2:"):
                # Extract current goal info from database
                old_data = {
                    'category': document['category'], 
                    'goal': document['goal_task'], 
                    'duedate': document['duedate'], 
                    'is_done': document['is_done']
                }                 
                # Form to edit goal
                with st.form(f'edit_goal_form_{document["timestamp"]}'):
                    new_category = st.text_input('Category', value=document['category'])
                    new_goal = st.text_input('Goal Task', value=document['goal_task'])
                    new_duedate = st.date_input('Due Date', value=document['duedate'])
                    get_new_goal_info = st.form_submit_button('Save Changes', type='primary', help='Make changes to the goal info you just selected.')
                    if get_new_goal_info:
                        # Validate: new goal doesn't already exist 
                        new_data = {
                            'category': new_category, 
                            'goal_task': new_goal, 
                            'duedate': date_to_datetime(new_duedate),
                        }
                        try:
                            # Convert duedate to saved form
                            duedate = date_to_datetime(new_duedate)
                            submit_result = edit_document_by_id(GOALS_LIST, document['_id'], new_data) 
                            if submit_result:
                                timer = time.Timer(.25, close_popover)
                                timer.start()                    
                        except Exception as e:
                            # Handle any exceptions that occur during the insertion process
                            display_message(f'Failed to save changes: {e}')
                            return None                        
    with col_delgoal:
        if st.button(":wastebasket:", key=f"delete_{document['_id']}", help="Delete the goal", use_container_width=True):
            # Implement delete functionality
            delete_document_by_id(GOALS_LIST, document['_id'])
    # Display goal information in separate columns
    with col_cat:
        st.write(document['category'])
    with col_goal:
        fields = ''         
        # Use the function to format the goal text
        for field in document:
            fields += f'field: {field}\n'
        # display_message(f"fields:\n\n {fields}")
        formatted_goal_text = format_goal_text(document)
        st.markdown(formatted_goal_text, unsafe_allow_html=True)
    with col_due:
        st.write(str(document['duedate'].date()))
        st.write(str(document['duedate'].strftime('%H:%M')))
    with col_timestamp:
        st.write(str(document['timestamp'].date()))
        st.write(str(document['timestamp'].strftime('%H:%M')))

def query_coll(filter_option, search_term):
    #st.write('Setting up filter options...')
    # Set query to exclude the option keys
    query = {"category": {"$not": {"$regex": "option"}}}    
    if filter_option.lower() == 'done':
        query['is_done'] = True
    elif filter_option.lower() == 'pending':
        query['is_done'] = False
    elif filter_option.lower() != 'all':
        raise ValueError("Invalid filter option")
        
    # if 'is_done' in query:  # Check if 'is_done' key is present in the query
    #     st.write(f"query['is_done']: {query['is_done']}")    
    if search_term:
        search_query = {
            "$or": [
                {"category": {"$regex": search_term, "$options": "i"}},
                {"goals_task": {"$regex": search_term, "$options": "i"}}
            ]
        }
        # Combine search query with existing query using "$and"
        query = {"$and": [query, search_query]}    
    #st.write(f'query: {query}')  # Check the final query    
    return query


def main():
    #st.sidebar.write('start main()')
    with st.sidebar:
        with st.form('search_form'):
            search_term = st.text_input('Search goals:')
            submitted = st.form_submit_button('Search', type='primary', help='Search in goals')
        if submitted:
            if st.button('Clear search', type='secondary'):
                st.session_state.search_term = ''
            st.session_state.search_term = search_term
            st.rerun()
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
        st.subheader('My Done SMART Goals!')
    with btn:
        add_goal()
        
    # Create a text index on the 'goal' field, only need to execute once (supposedly)    
    # First, list all indexes
    indexes = GOALS_LIST.list_indexes()
    for index in indexes:
        pass
        # st.write(f'\n\n index name: {index}')
    # Define the index you want to create
    index_spec = [('goal_task', 'text')]  

    # Specify the index name to check
    index_name = "goals_task_text_category_text"
    index_name = "goals_task_text"
    # Check if the index exists
    index_exists = any(index["name"] == index_name for index in GOALS_LIST.list_indexes())
    if not index_exists:
        # st.write(f"The index '{index_name}' does not exist!")
        GOALS_LIST.create_index([
        ('goals_task', 'text'),
        ('category', 'text'),
        # Add more fields as needed
    ])
    
    st.sidebar.write(f'st.session_state.sort: {st.session_state.sort}')
    st.sidebar.write(f'st.session_state.srt_order: {st.session_state.srt_order}')
    goal_list = GOALS_LIST.find().sort(st.session_state.sort, st.session_state.srt_order) 
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
        st.button('Category', 'sort_docs("goals", "category")')
        def sort_docs(coll, sort_field):
            if 'cat_sort' not in st.session_state:
                st.session_state['cat_sort'] = False
            if st.session_state['cat_sort']:
                st.session_state['cat_sort'] = False
            else:
                st.session_state['cat_sort'] = True
    with col_goal:
        'Goal Task'
    with col_due:
        'Due Date'
    with col_timestamp:
        'Set Date'
    for single_goal in goal_list:
        # display_message('listing all the goals in main()')
        render_goal(single_goal, False)

if __name__ == "__main__":
    main()