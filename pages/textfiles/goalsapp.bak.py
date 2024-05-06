import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta 
from streamlit_extras.stylable_container import stylable_container
from time import sleep

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
# Setup MongoDB client
DB = client['goals']
# Get all documents in goals collection
GOALS = DB['goal_list']
# Query MongoDB for unique values of the "category" field
CATEGORIES = GOALS.distinct("category")
# COUNTER variable for keys
COUNTER = 0

# # Define custom CSS style for the buttons
# button_style = """
#     <style>
#         div.stButton > button:first-child {
#             color: hotpink;
#             border-color: hotpink;
#             border-width: 2px;
#         }
#         div.stButton > button:first-child:hover {
#             color: pink;  
#             border-color: pink;  
#         }
#     </style>
# """
# # Display custom buttons
# st.markdown(button_style, unsafe_allow_html=True)

# Initialize session states
if 'selected_categories' not in st.session_state:
    st.session_state.selected_categories = [] 
    
if 'search_term' not in st.session_state:
    st.session_state.search_term = '' 
    
if 'sort_option' not in st.session_state:
    st.session_state.sort_option = ''
    
if 'sort_order' not in st.session_state:
    st.session_state.sort_order = ''

st.title('SMART Goals Journal App')

# Create an empty container at the top of the screen
message_container = st.empty()
sidebar_msg = st.sidebar.empty()
addgoal_form_container = st.sidebar.empty()
editgoal_form_container = st.sidebar.empty()

# Function to open sidebar when button is clicked
def on_button_click(button_text, help_text, callback):
    #COUNTER += 1
    #COUNTER_str = str(COUNTER)
    if st.button(button_text, help=help_text, on_click=callback):        
        sidebar_msg.success('Callback processed!')

def render_new_goal_form(timestamp=None, tomorrow=None):
    if timestamp is None:
        timestamp = datetime.now()
    if tomorrow is None:
        tomorrow = datetime.now() + timedelta(days=1)
    with addgoal_form_container.form(key='new_goal_form'):
        st.write('Add a new goal:')
        duedate = st.date_input('Due Date', tomorrow)
        category = st.text_input('Category')
        goal = st.text_input('Goal Task')
        save_goal_button = st.form_submit_button(label='Save Goal', help="Save the new goal")
        if save_goal_button:
             {'timestamp': timestamp,
                    'category': category,
                    'goal': goal,
                    'duedate': duedate,
                    'is_done': False}

    return None


def render_date_input(label, value):
    return st.date_input(label, value=value)


def render_text_input(label):
    return st.text_input(label)


def submit_new_goal_form(data):
    try:
        submit_result = add_new_document(GOALS, data)
        if submit_result:
            message_container.success("Document inserted successfully with id:", submit_result.inserted_id)
            return True
        else:
            message_container.warning("Failed to insert document.")
            return False
    except Exception as e:
        message_container.warning("Error occurred while inserting document:", e)
        return False


def show_add_new_goal_form():
    form_data = render_new_goal_form()
    if form_data is not None:
        return submit_new_goal_form(form_data)
    return False


# documents = list(GOALS.find())
# # Display the documents in a Streamlit component
# if documents:
#     st.write("List of Documents:")
#     for doc in documents:
#         st.write(doc)
# else:
#     st.write("No documents found in the collection.")
    
# GOALS.delete_many({})
#duedatetime1 = datetime.combine(duedate1, datetime.min.time())
# Check for datetime instance
#assert isinstance(duedatetime1, datetime), "duedatetime is not a datetime.datetime object"

    
# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())


add_btn, show_btn, sort_btn, srch_form = st.columns(4)
with add_btn:    
    # Create a button that opens the add goal form when clicked
    on_button_click("Add new goal", "Add a new goal to your journal", show_add_new_goal_form())
with show_btn:     
    # Filter dropdown for CATEGORIES
    # Add "All" option to the list of CATEGORIES
    CATEGORIES.insert(0, "All")
    selected = st.selectbox('Filter by:', key='cat', options=CATEGORIES, index=0)
    if selected:   
        st.session_state.selected_categories.extend(selected)
    # If "All" is selected or no category is selected, use all CATEGORIES
    if "All" in st.session_state.selected_categories or not st.session_state.selected_categories:
        st.session_state.selected_categories = CATEGORIES
    duedate_filter = st.date_input("Due Date", value=None)
    duedate_filter = date_to_datetime(duedate_filter)        
    timestamp_filter = st.date_input("Timestamp", value=None)
    timestamp_filter = date_to_datetime(timestamp_filter)
with sort_btn:
    # Display sort buttons in one column
    sort_by = st.selectbox("Sort by", ["Category", "Goal task", "Due Date", "Date Entered"])
    sort_order = st.selectbox("Sort Order", ["Ascending", "Descending"])
    # Update session_state variables for sorting
    if sort_by:
        st.session_state.sort_option = sort_by
    if sort_order:
        st.session_state.sort_order = sort_order
with srch_form:    
    # Create search form
    with st.form(key="srch_form"):
        search_term = st.text_input("Search goals")
        if st.form_submit_button(label='Search', help="Search for something in your goal journal"): 
            st.session_state.search_term = search_term
    
    
test_data = [
    [ False, 'goals', 'fix update not working']
    ,
    [ False, 'goals', 'change filter, sort, search to session_state' ]
    ,
    [ True, 'goals', 'add scratchout for done goals' ]
    ,
    [ True, 'goals', 'add undo button if done' ]
    ,
    [ False, 'calls', 'fred appt' ]
    ,
    [ False, 'calls', 'schedule surgery' ]
    ,
    [ False, 'calls', 'dentist appt me' ]
    ,
    [ False, 'calls', 'dentist appt charlie' ]
    ,
    [ False, 'goals', 'fix save goal button not working' ]
    ,
    [ True, 'goals', 'change button style' ]
    ,
    [ False, 'lfha', 'basic app' ]
    ,
    [ False, 'lfha', 'gamify - see trilium notes' ]
    ,
    [ True, 'daily', 'brush teeth' ]
    ,
    [ False, 'daily', 'rinse mouth' ]
    ,
    [ False, 'daily', 'take pills' ]
    ,
    [ False, 'daily', 'prayers' ]
    ,
    [ False, 'daily', 'scripture study' ]
    ,
    [ False, 'daily', 'THM 1 hour' ]
    ,
    [ False, 'daily', 'picoCTF 1 hour' ]
    ,
    [ True, 'daily', 'wash dishes' ]
    ,
    [ False, 'daily', 'make dinner' ]
    ,
    [ False, 'daily', 'clean table' ]
    ,
    [ False, 'daily', 'clean stove' ]
    ,
    [ False, 'daily', 'clean COUNTERer left' ]
    ,
    [ False, 'daily', 'clean COUNTERer middle' ]
    ,
    [ False, 'daily', 'clean COUNTERer right' ]
    ,
    [ False, 'weekly', 'organize door wall shelves' ]
    ,
    [ False, 'weekly', 'organize AC shelves' ]
    ,
    [ True, 'weekly', 'order groceries' ]
    ,
    [ False, 'weekly', 'organize walkup shelves' ]
    ,
    [ False, 'daily', 'clean fruit basket' ]
    ,
    [ False, 'daily', 'kitchen trash out/new bag' ]
    ,
    [ False, 'daily', 'liv rm trash out/new bag' ]
    ,
    [ False, 'daily', 'bathroom trash out/new bag' ]
    ,
    [ False, 'daily', 'kitchen recycles out' ]
    ,
    [ False, 'daily', 'bedroom recycles out' ]
    ,
    [ False, 'daily', 'bedroom trash out/new bag' ]
    ,
    [ False, 'daily', 'clean bathroom COUNTERer' ]
    ,
    [ False, 'daily', 'clean toilet' ]
    ,
    [ False, 'daily', 'sweep bathroom ' ]
    ,
    [ False, 'daily', 'sweep kitchen' ]
    ,
    [ False, 'daily', 'mop bathroom' ]
    ,
    [ False, 'daily', 'mop kitchen' ]
    ,
    [ False, 'daily', 'puppy pads' ]
    ,
    [ False, 'daily', 'sweep liv rm' ]
    ,
    [ False, 'daily', 'mop liv rm' ]
    ,
    [ False, 'daily', 'move sofa' ]
    ,
    [ False, 'zzzzz', 'default' ]
    ,
    [ False, 'zzzzz', 'default' ]
    ,
    [ False, 'zzzzz', 'default' ]
    ,
    [ False, 'zzzzz', 'default' ]
    ,
    [ False, 'zzzzz', 'default' ]
    ]


def add_new_document(collection, data):
    saved_id = collection.insert_one(data)
    message_container.success(f'saved_id: {saved_id}')
    return saved_id

    
def delete_all_documents(collection):
    delete_all_result = collection.delete_many({})
    # Update the content of the container with your message
    message_container.success(f"Deleted {delete_all_result.deleted_COUNTER} documents from the collection.")
    st.rerun()  # Rerun the app to reflect changes
    

# TODO:  TURN THIS OFF AFTER DEBUGGING DONE!!!
#delete_all_documents(GOALS)
# ADD MY DEFAULT GOALS
for info in test_data:
    newgoal = {'timestamp' : datetime.now(), 'category' : info[1], 'goal' : info[2], 'duedate' : date_to_datetime(datetime.now().date() + timedelta(days=1)) , 'is_done' : info[0] }
    newgoal_text = ''
    for field in newgoal:
        newgoal_text += field
        newgoal_text += '\n'
        
    sidebar_msg.success('newgoal: \n' + newgoal_text)
    test_add_function = add_new_document(GOALS, newgoal)
    #saved_id = GOALS.insert_one(newgoal)
#message_container.success(f'saved_id: {saved_id}')
message_container.success('test_add_function: ' + str(test_add_function.inserted_id))
    
    
def delete_document_by_id(collection, document_id):
    delete_result = collection.delete_one({"_id": document_id})
    if delete_result.deleted_COUNTER == 1:        
        message_container.success(f"Document with ID {document_id} deleted successfully.")
    else:        
        message_container.warning(f"No document found with ID {document_id}.")
        
            
def edit_document(document_id):                    
    sidebar_msg.warning('edit_document function invoked!')
    sleep(3)
    # Fetch the document to edit
    document = GOALS.find_one({"_id": document_id})
    sidebar_msg.warning(document)
    sleep(3)
    with addgoal_form_container:
        # Display the document data in an editable form
        update_data = {}
        placeholders = {}  # Placeholder dictionary to store st.empty() objects
        with st.form(key="edit_form"):
            for field, value in document.items():
                if field != "_id":
                    sidebar_msg.warning(f'field: {field}')
                    sleep(3)
                    if isinstance(value, bool):
                        update_data[field] = st.checkbox(field, value)
                    elif isinstance(value, str):
                        update_data[field] = st.text_input(field, value)
                    elif isinstance(value, int):
                        update_data[field] = st.number_input(field, value=value)
                    elif isinstance(value, float):
                        update_data[field] = st.number_input(field, value=value)
                    elif isinstance(value, list):
                        update_data[field] = st.multiselect(field, value)
                    elif isinstance(value, dict):
                        sidebar_msg.warning(f"Skipping field '{field}' of type 'dict'.")
                        sleep(3)
                    else:
                        sidebar_msg.warning(f"Skipping field '{field}' of unknown type.")
                        sleep(3)
                        
            with stylable_container(key="unique-edit", css_styles="""
                { [data-testid="baseButton-secondary"] { color: hotpink; border-color: hotpink; border-width: 2px; } }
                """):
                # Update the document in the collection
                if st.form_submit_button(label='Save Changes', help="Save the edits you made"):               
                    sidebar_msg.warning(update_data)
                    sleep(3)
                    update_query = {"_id": document_id}
                    update_operation = {"$set": update_data}
                    GOALS.update_one(update_query, update_operation)
                    sidebar_msg.success("Document updated successfully.")
                    sleep(3)

        
def toggle_mark_as_done(collection, document_id):
    # Retrieve the current document
    current_document = collection.find_one({"_id": document_id})
    if current_document:
        # Toggle the value of the "is_done" field
        new_value = not current_document.get("is_done", False)
        # Update the document in the collection
        collection.update_one({"_id": document_id}, {"$set": {"is_done": new_value}})
        return new_value  # Return the new value of "is_done"
    else:
        return None  # Document not found


# Define a function to format the goal text based on is_done value
def format_goal_text(goal):
    if goal['is_done']:
        return f"<del>{goal['goal']}</del>"
    else:
        return goal['goal']


def render_goal(goal):
    # Create separate columns for each field and button
    col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1, 2, 3, 2, 2])

    # Add buttons for editing, deleting, and marking as done
    with col_markdone:
        if goal['is_done']:
            icon = ":repeat_one:"
            help_text = "Undo goal achievement"
        else:
            icon = ":white_check_mark:"
            help_text = "Mark the goal as achieved"
        with stylable_container(key="unique-done", css_styles="""
            { [data-testid="baseButton-secondary"] { color: prussian; border-color: prussian; border-width: 2px; } }
            """):    
            if st.button(icon, key=f"mark_done_{goal['_id']}", help=help_text, use_container_width=True):
                # Toggle mark as done
                toggle_mark_as_done(GOALS, goal['_id'])
                st.rerun()  # Rerun the app to reflect changes
    with col_edit:
        with stylable_container(key="unique-edit", css_styles="""
            { [data-testid="baseButton-secondary"] { color: prussian; border-color: prussian; border-width: 2px; } }
            """):
            if st.button(":pencil2:", key=f"edit_{goal['_id']}", help="Edit the goal", use_container_width=True):                    
                sidebar_msg.warning('edit_document button invoked!')
                sleep(3)
                # Implement edit functionality
                st.write("Edit Goal")
                edit_document(goal['_id'])
                st.rerun()  # Rerun the app to reflect changes        
    with col_delgoal:
        with stylable_container(key="unique-delete", css_styles="""
            { [data-testid="baseButton-secondary"] { color: prussian; border-color: prussian; border-width: 2px; } }
            """):
            if st.button(":wastebasket:", key=f"delete_{goal['_id']}", help="Delete the goal", use_container_width=True):
                # Implement delete functionality
                delete_document_by_id(GOALS, goal['_id'])
                st.rerun()  # Rerun the app to reflect changes
    # Display goal information in separate columns
    with col_cat:
        st.write(goal['category'])
    with col_goal:         
        # Use the function to format the goal text
        formatted_goal_text = format_goal_text(goal)# Display the formatted goal text using st.markdown
        st.markdown(formatted_goal_text, unsafe_allow_html=True) 
        #st.write(formatted_goal_text)
    with col_due:
        st.write(str(goal['duedate'].date()))
    with col_timestamp:
        st.write(str(goal['timestamp'].date()))


# Main function
def main():        
    with st.sidebar:
        # Emergency button to delete all goals, for debugging only
        with stylable_container(key="unique-delete-all", css_styles="""
            { [data-testid="baseButton-secondary"] { color: hotpink; border-color: hotpink; border-width: 2px; } }
            """):
            if st.button("Delete All Documents", key="delete_all_docs"):
                delete_all_documents(GOALS)    
    


    with stylable_container(key="unique", css_styles="""
        { [data-testid="baseButton-secondary"] { color: hotpink; border-color: hotpink; border-width: 2px; } }
        """):
        st.subheader('My SMART Goals Journal')
        # Fetch goals based on filters, search, and sort criteria
        filter_query = {}

        # Apply filters
        if st.session_state.selected_categories and "All" not in st.session_state.selected_categories:
            filter_query["category"] = {"$in": st.session_state.selected_categories}
        if duedate_filter:
            filter_query["duedate"] = {"$eq": st.session_state.duedate_filter}
        if timestamp_filter:
            filter_query["timestamp"] = {"$eq": st.session_state.timestamp_filter}    
            
        # Create a text index on the 'goal' field, only need to execute once (supposedly)
        # GOALS.create_index([('goal', 'text')])
            
        # Apply search
        if search_term:
            filter_query["$text"] = {"$search": search_term}
        # st.write('filter_query: ', filter_query)
        # Fetch goals from MongoDB based on the filter query
        fields = {'_id': 1, 'category':1, 'goal': 1, 'is_done': 1, 'timestamp': 1, 'duedate': 1}
        filtered_goals = GOALS.find(filter_query, fields)
        # filtered_goals

        # Apply sorting
        if sort_by == "Category":
            sort_field = "category"
        elif sort_by == "Goal Task":
            sort_field = "goal"
        elif sort_by == "Due Date":
            sort_field = "duedate"
        elif sort_by == "Date Entered":
            sort_field = "timestamp"
                    
        sort_field = sort_by.lower().replace(" ", "_")
        sort_order = -1 if st.session_state.sort_order == "Descending" else 1

        # Sort goals based on the selected field and direction
        goal_list = filtered_goals.sort(sort_field, sort_order)
        #goal_list
        
        # # Convert MongoDB cursor to list of dictionaries
        goal_list = list(goal_list)
        # goal_list

        # # Display the data table
        # if len(goal_list) > 0:
        #     st.dataframe(goal_list)  # Display the data table
        # else:
        #     st.write("No goals found in database.")

        col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1, 2, 3, 2, 2])
        with col_markdone:
            ''
        with col_edit:
            ''
        with col_delgoal:
            ''
        with col_cat:
            'Category'
        with col_goal:
            'Goal Task'
        with col_due:
            'Due Date'
        with col_timestamp:
            'Set Date'   
        for goal in goal_list:
            render_goal(goal)

if __name__ == "__main__":
    main()
