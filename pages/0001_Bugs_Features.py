from mods.db import *

# Page Constants
PAGE_SUBHEADER = 'Bugs and Features'

SEARCH_FORM_DATA = {
    'form_key': 'search_form',
    'form_button_label': 'Submit',
    'fields': {
        'search_goals': {
            'type': 'text',
            'label': 'Search goals:'
        },
        'filter_choice': {
            'type': 'selectbox',
            'label': 'Filter by:',
            'options': ['All', 'Done', 'Pending']
        }
    }
}


# SESSION VARIABLES
if 'counter' not in st.session_state:
       st.session_state.counter = 1

if 'search_terms' not in st.session_state:
    st.session_state.search_terms = ['bug']

if 'filter_choice' not in st.session_state:
    st.session_state.filter_choice = 'Pending'

if 'srt_by' not in st.session_state:
    st.session_state.srt_by = 'timestamp' 
    
if 'srt_ord' not in st.session_state:
    st.session_state.srt_ord = -1
    
if 'user_role' not in st.session_state:
    st.session_state.user_role = ''

# {'category': {'$regex': 'apps', '$options': 'i'}},

def main():
  # custom_print('inside bugs_features.main()')
    st.subheader(f'My SMART Goals Journal: {PAGE_SUBHEADER}')
    col1, col2 = st.columns([2, 7])
    with col1:
        add_goal()
    with col2:
        ''
        '♻️ = recycle the goal - if this is clicked, the goal will become repeatable'
        '🌓 = marked as repeatable, recyle has been clicked - clicking it will make the goal a one-time goal'
        'When a recycle goal is marked done, it will be added as an achieved goal to the journal list.'

    #build_form_box(form_data)
  # custom_print(f'invoking build_search_box!')
    build_search_box(SEARCH_FORM_DATA)

  # custom_print(f'st.session_state.filter_choice: {st.session_state.filter_choice}')
  # custom_print(f'st.session_state.search_terms: {st.session_state.search_terms}')
  # custom_print(f'st.session_state.srt_by: {st.session_state.srt_by}')    
  # custom_print(f'st.session_state.srt_ord: {st.session_state.srt_ord}')
                  
    filter_query = set_filter_query(st.session_state.filter_choice, st.session_state.search_terms)  
  # custom_print(f'filter_query: {filter_query}')

  # custom_print(f'st.session_state.filter_choice: {st.session_state.filter_choice}')
  # custom_print(f'st.session_state.search_terms: {st.session_state.search_terms}')
  # custom_print(f'st.session_state.srt_by: {st.session_state.srt_by}')    
  # custom_print(f'st.session_state.srt_ord: {st.session_state.srt_ord}')
  # custom_print(f'ALL_GOALS_COLL: {ALL_GOALS_COLL}')
    FILTERED_BUG_FEATURE_LIST = sorted_records_list(ALL_GOALS_COLL, filter_query, st.session_state.srt_by, st.session_state.srt_ord)

  # custom_print('about to invoke bugs_features.render_goals()')

    if FILTERED_BUG_FEATURE_LIST is None:
      custom_print("FILTERED_BUG_FEATURE_LIST is None")
        #FILTERED_BUG_FEATURE_LIST = []

  # custom_print(f'FILTERED_BUG_FEATURE_LIST: {FILTERED_BUG_FEATURE_LIST}')

    render_goals(FILTERED_BUG_FEATURE_LIST)


if __name__ == "__main__":
    main()
