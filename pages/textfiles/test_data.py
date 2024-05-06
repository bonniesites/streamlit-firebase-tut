
   
test_data = [
    [ True, 'goals', 'fix update not working']
    ,
    [ False, 'goals', 'change filter, sort, search to session_state' ]
    ,
    [ True, 'goals', 'add scratchout for mark done' ]
    ,
    [ True, 'goals', 'add undo button if done' ]
    ,
    [ False, 'calls', 'fred appt' ]
    ,
    [ False, 'calls', 'schedule surgery' ]
    ,
    [ True, 'calls', 'dentist appt me' ]
    ,
    [ True, 'calls', 'dentist appt charlie' ]
    ,
    [ True, 'goals', 'fix save goal button not working' ]
    ,
    [ True, 'goals', 'change button style' ]
    ,
    [ False, 'lfha', 'basic app' ]
    ,
    [ False, 'lfha', 'gamify - see trilium notes' ]
    ,
    [ False, 'repeat', 'brush teeth' ]
    ,
    [ False, 'repeat', 'rinse mouth' ]
    ,
    [ False, 'repeat', 'take pills' ]
    ,
    [ False, 'repeat', 'prayers' ]
    ,
    [ False, 'repeat', 'scripture study' ]
    ,
    [ False, 'repeat', 'shower' ]
    ,
    [ False, 'repeat', 'THM 1 hour' ]
    ,
    [ False, 'repeat', 'picoCTF 1 hour' ]
    ,
    [ False, 'repeat', 'wash dishes' ]
    ,
    [ False, 'repeat', 'make dinner' ]
    ,
    [ False, 'repeat', 'clean table' ]
    ,
    [ False, 'repeat', 'clean stove' ]
    ,
    [ False, 'repeat', 'clean counter left' ]
    ,
    [ False, 'repeat', 'clean counter middle' ]
    ,
    [ False, 'repeat', 'clean counter right' ]
    ,
    [ False, 'weekly', 'organize door wall shelves' ]
    ,
    [ False, 'weekly', 'organize AC shelves' ]
    ,
    [ True, 'weekly', 'order groceries' ]
    ,
    [ False, 'weekly', 'organize walkup shelves' ]
    ,
    [ False, 'repeat', 'clean fruit basket' ]
    ,
    [ False, 'repeat', 'kitchen trash out/new bag' ]
    ,
    [ False, 'repeat', 'liv rm trash out/new bag' ]
    ,
    [ False, 'repeat', 'bathroom trash out/new bag' ]
    ,
    [ False, 'repeat', 'kitchen recycles out' ]
    ,
    [ False, 'repeat', 'bedroom recycles out' ]
    ,
    [ False, 'repeat', 'bedroom trash out/new bag' ]
    ,
    [ False, 'repeat', 'clean bathroom counter' ]
    ,
    [ False, 'repeat', 'clean toilet' ]
    ,
    [ False, 'repeat', 'sweep bathroom ' ]
    ,
    [ False, 'repeat', 'sweep kitchen' ]
    ,
    [ False, 'repeat', 'mop bathroom' ]
    ,
    [ False, 'repeat', 'mop kitchen' ]
    ,
    [ False, 'repeat', 'puppy pads' ]
    ,
    [ False, 'repeat', 'sweep liv rm' ]
    ,
    [ False, 'repeat', 'mop liv rm' ]
    ,
    [ False, 'repeat', 'move sofa' ]
    ,
    [ True, 'goals', 'fix pink boxes on action icons' ]
    ,
    [ False, 'goals', 'repeat function: search for todays date, if not found, when mark done, create a new done goal with todays date as done.' ]
    ,
    [ False, 'goals', 'add date done' ]
    ,
    [ False, 'lfha', 'family tree' ]
    ,
    [ False, 'lfha ', 'convert from mongo doc to list' ]
    ,
    [ False, 'goals', 'change category in add/edit forms to dropdown from unique categories in db' ]
    ,
    [ True, 'goals', 'add btn for add category in add/edit forms' ]
    ,
    [ False, 'goals', 'button column headings to sort asc/desc' ]
    ,
    [ False, 'calls', 'Auntie' ]
    ,
    [ False, 'calls', 'oral surgery appt(s)' ]
    ,
    [ False, 'lists', 'things  ' ]
    ,
    [ False, 'apps', 'ingredients/shoppingList/recipes cooking app, use AI chatbot to find recipes from internet?' ]
    ,
    [ False, 'goals', 'implement  1 search' ]
    ,
    [ False, 'goals', 'implement 2 filter' ]
    ,
    [ False, 'goals', 'implement 3 sort' ]
    ,
    [ False, 'goals', 'implement 4 change font color if overdue from subracting duedate from donedate (if < 0, late)' ]
    ,
    [ False, 'calls', 'Cuz Wendy stuff in trilium under for app project' ]
    ,
    [ False, 'goals', 'gamify: private and public leaderboards with stats, points, badges' ]
    ,
    [ False, 'goals', 'share feature, from any page, like leaderboard' ]
    ,
    [ False, 'goals', 'implement single category or subcategories {symptom/food journal} btn to CRUD new subcategory to/from a collection' ]
    ,
    [ False, 'apps', 'small biz modules/subscription paypal/stripe, how to tie to user account as paid' ]
    ,
    [ False, 'apps', 'plant identifier for iPhone, notes/subcategories/tags highlighted diff colors, like edible, poisonous, etc' ]
    ,
    [ False, 'goals', 'feature: SMART how are they done? specific=task, measurable=progress bar? other?, achievable/accountable=user to be notified, relevant=parent goal?, timebound=duedate' ]
    ,
    [ False, 'goals', 'accountable=mentor, person who will be notified if duedate passes before completion or completion before duedate' ]
    ,
    [ False, 'goals', 'relevance-parent goal, chores done is parent for individual chores, shown by parent goal progress bar' ]
    ,
    [ False, 'goals', 'measurable-progress for the parent goal with each subtask done' ]
    ,
    [ False, 'goals', 'list display has 2 rows for each goal: progress bar and row with edit, delete, markdone' ]
    ,
    [ False, 'goals', 'how to set progress bar for parent from subtasks?' ]
    ,
    [ False, 'apps', 'custom theme per user' ]
    ,
    [ False, 'goals', 'each parent goal will have a button Show instead of Done that either opens expander or popover that shows sublist of subgoals with own progress bars, subgoals will have Done button' ]
    ,
    [ False, 'goals', 'will need special popover code that doesnt auto close it, dict in session var that has ids maybe?' ]
    ,
    [ False, 'school', 'Put together Senior Project plan to submit' ]
    ,
    [ False, 'school', 'pay off $188 balance' ]
    ,
    [ True, 'goals', 'close popovers automatically if submitted' ]
    ,
    [ False, 'goals', 'prioritize feature' ]
    ,
    [ False, 'goals', 'fix text data not entered' ]
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
    ,
    [ False, 'zzzzz', 'default' ]
    ,
    [ False, 'zzzzz', 'default' ]
    ,
    [ False, 'zzzzz', 'default' ]
]

