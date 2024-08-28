from mods.imports import *
from mods.db_functions import *





# DATABASES
GOALS_DB = CLIENT.goals
CHARLIE_DB = CLIENT.charlie
REDDIT_CLONE_DB = CLIENT.reddit_clone
RUSH_DB = CLIENT.rushGrather

# COLLECTIONS
ALL_GOALS_COLL = GOALS_DB.goals_list
OPTIONS_COLL = GOALS_DB.options
CHARLIE_COLL = GOALS_DB.CHARLIE_COLL
REDDIT_POSTS_COLL = REDDIT_CLONE_DB.posts
REDDIT_USERS_COLL = REDDIT_CLONE_DB.users

# CURSORS
ALL_GOALS_CURSOR = ALL_GOALS_COLL.find()
DONE_GOALS_CURSOR = ALL_GOALS_COLL.find({"is_done":True})
PENDING_GOALS_CURSOR = ALL_GOALS_COLL.find({"is_done":False})


# LISTS
ALL_GOALS_LIST = list(ALL_GOALS_CURSOR)

coll_count = ALL_GOALS_COLL.count_documents({})  # This will work with older versions of PyMongo
#print(f"Number of colls in ALL_GOALS_CURSOR: {coll_count}")

cursor_count = len(ALL_GOALS_LIST)

#print(f"Number of documents in ALL_GOALS_CURSOR: {cursor_count}")

# TODO: switch to categories table in db

CATEGORIES = ALL_GOALS_COLL.distinct('category')

  
def change_sort_order():
    st.session_state.srt_order *= -1

def sort_record_list(list):
    return list.sort([(st.session_state.srt_by, st.session_state.srt_order)])

def backup_collection(db_name, collection_name):
    # Create a temporary directory to store the backup files
    temp_dir = tempfile.mkdtemp()
    # Backup MongoDB collection
    backup_file = os.path.join(temp_dir, f"{db_name}-{collection_name}_backup_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".bson")
    os.system(f"mongodump --db your_database --collection {collection_name} --out {temp_dir}")
    # Create a ZIP file containing the backup files
    zip_file = os.path.join(temp_dir, f"{collection_name}_backup.zip")
    with ZipFile(zip_file, 'w') as zipObj:
        for folderName, _, filenames in os.walk(temp_dir):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.relpath(filePath, temp_dir))
    return zip_file

# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())

def add_new_document(_coll, data):
    try:
        # Attempt to insert the document
        new_id = _coll.insert_one(data)
        # Display success message
        MSG_CONTAINER.success(f'Document added successfully with id: {new_id.inserted_id}')
        return new_id
        st.rerun()  # Refresh the goal journal
    except Exception as e:
        # Handle any exceptions that occur during the insertion process
        MSG_CONTAINER.warning(f'Failed to save document: {e}')
        return None

    
def check_existing_doc(coll, new_data):
    existing_data = coll.find_one(new_data)
    if existing_data:
        MSG_CONTAINER.success("Data already exists in the collection")
    else:
        MSG_CONTAINER.warning("Data does not exist in the collection")
    return existing_data


def check_and_add_field(goal, field):
    #custom_print('inside mods.db.check_and_add_field()')
    update_ready = False
    if field not in goal:
        if field == 'is_done' or field == 'is_repeat':
            goal[field] = False 
        elif field == 'goal_task':
            goal[field] = ''
            update_ready = True
    else:
        return goal[field]
    if update_ready:
        ALL_GOALS_COLL.update_one({'_id': goal['_id']}, {'$set': goal})
        return goal[field]
       
def toggle_bool(coll, doc_id, bool_field):
    #custom_print('inside mods.db.toggle_bool()')
    current_goal = get_goal(coll, doc_id)
    if current_goal:
        new_value = not current_goal.get(bool_field, False)
        coll.update_one({'_id': doc_id}, {'$set': {bool_field: new_value}})
        return new_value 
    else:
        return None 

def get_goal(coll, doc_id):
    #custom_print('inside mods.db.get_goal()')
    return coll.find_one({'_id': doc_id})

def query_list(coll, filter_option, search_terms):
    #custom_print('inside mods.db.query_list()')
    query = {
        '$and': [
            {'$or': [
                {'category': {'$regex': search_terms, '$options': 'i'}},
                {'goal_task': {'$regex': search_terms, '$options': 'i'}}
            ]}
        ]
    }
    if filter_option == 'done':
        query['$and'].insert(0, {'is_done': True})
    elif filter_option == 'pending':
        query['$and'].insert(0, {'is_done': False})
    results = coll.find(query).sort('timestamp', -1)
    return list(results)


def format_goal_text(goal):
    if goal['is_done']:
        return f"<del>{goal['goal_task']}</del>" if goal['is_done'] else goal['goal_task']
    else:
        return goal['goal_task']
    

def render_goal(goal):
    col_count, col_markdone, col_edit, col_delgoal, col_repeat, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1.5, 1, 1, 2.5, 4, 2, 2], gap='small')

    with col_count:        
        st.write(st.session_state.counter)
        st.session_state.counter += 1
    counter_box.write(f'Goal count = {st.session_state.counter}')
    
    with col_repeat:
        if goal['is_repeat']:
            icon = '🌓'
            help_text = 'Mark the goal as repeatable'
        else:
            icon = '♻️'
            help_text = "Mark the goal as NOT repeatable"
        repeat_key = f"repeat_{goal['_id']}"
        if st.button(icon, key=repeat_key, help=help_text, use_container_width=False):
            toggle_bool(ALL_GOALS_COLL, goal['_id'],'is_repeat')
            st.rerun()

    with col_markdone:
        if 'is_done' in goal and goal['is_done']:
            icon = '💫'
            help_text = 'Undo goal achievement'
        else:
            icon = '🔄'
            help_text = "Mark the goal as achieved"
        mark_key = f"mark_done_{goal['_id']}"
        if st.button(icon, key=mark_key, help=help_text, use_container_width=False):
            toggle_bool(ALL_GOALS_COLL, goal['_id'],'is_done')
            st.balloons()
            st.rerun()

    with col_edit: 
        edit_goal(goal) 

    with col_delgoal:
        if st.button(":wastebasket:", key=f"delete_{goal['_id']}", help="Delete the goal", use_container_width=True):
            # Implement delete functionality
            delete_document_by_id(ALL_GOALS_COLL, goal['_id'])

    with col_cat:
        st.write(f"{goal['category']},  \n {goal['subcategory']},  \n {goal['subsubcategory']}")

    with col_goal:
        fields = ''         
        # Use the function to format the goal text
        for field in goal:
            fields += f'field: {field}\n'
        # display_message(f"fields:\n\n {fields}")
        formatted_goal_text = format_goal_text(goal)
        st.markdown(formatted_goal_text, unsafe_allow_html=True)
        # custom_print(f" \n goal['is_done']: {goal['is_done']} \n ")
        # if goal['is_done']:
        #     goal_task = format_goal_text(goal['goal_task'])
        # else: 
        #     goal_task = goal['goal_task']
        #st.write(format_goal_text(goal))

    with col_due:
        st.write(str(goal['duedate'].date()))
        st.write(str(goal['duedate'].strftime('%H:%M')))

    with col_timestamp:
        st.write(str(goal['timestamp'].date()))
        st.write(str(goal['timestamp'].strftime('%H:%M')))
        
    #print('inside mods.db.goal rendered!') 

def add_goal():
    #custom_print('inside mods.db.add_goal()')
    with st.popover('  \+ &nbsp;&nbsp;  Add &nbsp; :new: &nbsp; goal: &nbsp;&nbsp; \+ '):
        with st.form('add_goal_form'):
            st.write('Add a new goal:')
            col_left, col_right = st.columns(2)
            with col_left:
                category = st.text_input('Category', value='apps')
                subcategory = st.text_input('Subcategory', value='bizwhiz')
                subsubcategory = st.text_input('Sub Subcategory', 'bug')
                goal_task = st.text_input('Goal Task', value='fix: ')
            with col_right:
                duedate = date_to_datetime(st.date_input('Due Date', value=datetime.now() + timedelta(days=1)))
                new_state = st.checkbox('Done?', value=False)
                new_repeat = st.checkbox('Repeatable?', value=False)
                #st.write('Inside the form')
                submitted = st.form_submit_button('Save Goal')
                if submitted:
                    #timer = threading.Timer(0.25, close_popover)
                    #timer.start() 
                    # TODO:  use lists as smart typing dropdowns?   
                    goal_data = {
                        'timestamp': datetime.now(), 
                        'category': category, 
                        'subcategory': subcategory, 
                        'subsubcategory': subsubcategory,  
                        'goal_task': goal_task, 
                        'duedate': date_to_datetime(duedate), 
                        'is_done': new_state,
                        'is_repeat' : new_repeat,
                    }                
                    submit_result = add_new_document(ALL_GOALS_COLL, goal_data)
                    if submit_result:
                        st.write('Goal saved successfully!')
                    else:
                        st.warning('Goal not saved!')

def edit_goal(goal):       
        #print('inside mods.db.edit_goal()')
        with st.popover(":pencil2:", use_container_width=False):
            old_data = {
                'category': goal.get('category', ''), 
                'subcategory': goal.get('subcategory', ''), 
                'subsubcategory': goal.get('subsubcategory', ''),
                'goal': goal.get('goal_task', ''), 
                'duedate': goal.get('duedate', datetime.now()), 
                'is_done': goal.get('is_done', False),
                'is_repeat': goal.get('is_repeat', False),  # Safely access the is_repeat key
            }                 
            goal_key = f"goal_{goal['_id']}"
            with st.form(goal_key):
                col_left2, col_right2 = st.columns(2)
                with col_left2:
                    new_category = st.text_input('Category', value=old_data['category'] or 'app')
                    new_subcategory = st.text_input('Subcategory', value=old_data['subcategory'] or 'bizwhiz')
                    new_subsubcategory = st.text_input('Subsubcategory', value=old_data['subsubcategory'] or 'bug_feature')                
                with col_right2:
                    new_goal = st.text_input('Goal Task', value=old_data['goal'] or 'feature:   add or fix: ')
                    new_duedate = st.date_input('Due Date', value=old_data['duedate'] or datetime.now())
                    new_done = st.checkbox('Is Done?', value=old_data['is_done'] or False)
                    new_repeat = st.checkbox('Is Repeatable?', value=old_data['is_repeat'] or False)
                    submitted2 = st.form_submit_button('Save Changes')
                    if submitted2:
                        # TODO: Validate, check that new goal_task doesn't already exist
                        new_data = {
                            'category': new_category,
                            'subcategory': new_subcategory, 
                            'subsubcategory': new_subsubcategory,  
                            'goal_task': new_goal, 
                            'duedate': date_to_datetime(new_duedate),
                            'is_repeat': new_repeat
                        }
                        try:
                            # Convert duedate to saved form
                            duedate = date_to_datetime(new_duedate)
                            submit_result = edit_document_by_id(ALL_GOALS_COLL, goal['_id'], new_data) 
                            if submit_result:
                                custom_print(f' \n submit_result: {submit_result}')
                                timer = time.Timer(.25, close_popover)
                                timer.start()                    
                        except Exception as e:
                            # Handle any exceptions that occur during the insertion process
                            st.warning(f'Failed to save changes: {e}')
                            return None

def render_goals(list):
    #custom_print('inside mods.db.render_goals()')
    col_count, col_cat, col_goal, col_due, col_timestamp = st.columns([5, 2.5, 4, 2, 2], gap='small')

    with col_count:
        'Goal count and operations'
    with col_cat:
        # Button to sort goals by category using session variables to hold sort_column and asc/desc
        st.button('Category', 'query_list(ALL_GOALS_COLL, st.session_state.search_terms, st.session_state.filter_choice)')
        
    with col_goal:
        'Goal Task'
    with col_due:
        'Due Date'
    with col_timestamp:
        'Set Date'
    st.session_state.counter = 1
    for single_goal in list:
        #custom_print(f'  \n single_goal: {single_goal} \n ')
        #custom_print('listing all the goals in main()')
        render_goal(single_goal)

def refresh_goals(list):
    custom_print('inside mods.db.refresh_goals()')
    if st.button('Refresh Goals List'):
        render_goals(list)
