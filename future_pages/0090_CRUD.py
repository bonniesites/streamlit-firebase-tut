
from mods.data_processing import *

categories_collection = GOALS_DB.categories

# # TODO:
# add search
# add filters
# add sort asc/desc 
# add date done when marked done everytime
# how/when to check for various bonuses 
# add +10 points to current_points variable on completion of tasks, include check for bonuses
# save high scores to users document
# add personal dashboard with leaderboard scores
# high scores: daily, weekly, monthly, year-to-date, total, daily average, d-w-m-y-t on-time 
# add time bonus-tier of times before duedate
# add time penalty-if after duedate, deduct x points
# add consecutive on-time bonus tiers
# add no reminders bonus (a/k/a without being asked)
# add on-time time left bonus
# add all opted in users leaderboard, same high scores in a nice table
# add cheat resistance        

PAGE_HEADER = 'Home'
PAGE_SUBHEADER = 'SMART Goal Journal & Game'
SITE_TITLE = f'SMART Habits | {PAGE_HEADER}'

MENU_ITEMS = {
       'Get Help': '/',
       'Report a bug': '/report_bug',
       'About': '# Add text here.'
}
    
# TODO: if logged in, show logout button
if st.sidebar.button("Logout", key='logout_btn'):
    logout()

        
st.session_state.show_popover = False

# Pydantic model for Category
class Category(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="id")
    category: str

# CRUD operations for Category
class CategoryCRUD:
    @staticmethod
    def create(category: Category) -> str:
        category_dict = category.dict(exclude={"id"})
        result = categories_collection.insert_one(category_dict)
        return str(result.inserted_id)

    @staticmethod
    def read() -> list[Category]:
        categories = categories_collection.find()
        return [Category(**category) for category in categories]

    @staticmethod
    def update(category_id: str, category: Category) -> int:
        category_dict = category.dict(exclude={"id"})
        result = categories_collection.update_one({"_id": ObjectId(category_id)}, {"$set": category_dict})
        return result.modified_count

    @staticmethod
    def delete(category_id: str) -> int:
        result = categories_collection.delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count
    
# Pydantic model for Goal
class Goal(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    timestamp: datetime = datetime.now()
    category: str
    goal_task: str
    is_done: bool = False
    duedate: datetime
    is_repeat: bool

# CRUD operations for Goal
class GoalCRUD:
    @staticmethod
    def create(goal: Goal) -> str:
        goal_dict = goal.dict(exclude={"id"})
        result = goals_collection.insert_one(goal_dict)
        return str(result.inserted_id)

    @staticmethod
    def read() -> list[Goal]:
        goals = goals_collection.find()
        return [Goal(**goal) for goal in goals]

    @staticmethod
    def update(goal_id: str, goal: Goal) -> int:
        goal_dict = goal.dict(exclude={"id"})
        result = goals_collection.update_one({"_id": ObjectId(goal_id)}, {"$set": goal_dict})
        return result.modified_count

    @staticmethod
    def delete(goal_id: str) -> int:
        result = goals_collection.delete_one({"_id": ObjectId(goal_id)})
        return result.deleted_count

# Streamlit UI
st.title("SMART Habits")
st.subheader("A SMART Goals Journal and Game")

col_goal, col_cat = st.columns(2)
with col_cat:
    # Add category (modal form)
    with st.popover('\+ category'):
        with st.form("Add New Category"):
            new_category_name = st.text_input("Category Name")
            if st.form_submit_button("Save"):
                if new_category_name:
                    new_category = Category(category=new_category_name)
                    category_id = CategoryCRUD.create(new_category)
                    st.success(f"Category '{new_category_name}' added with ID: {category_id}")
                    # Close modal                
                    st.session_state.show_popover = not st.session_state.show_popover
                else:
                    st.warning("Please enter a category name")
with col_goal:            
    with st.popover('\+ goal'):            
        # Create form
        with st.form('add_goal'):
            goal_task = st.text_input("Goal Task")
            duedate = st.date_input("Due Date")
            is_repeat = st.checkbox("Repeat?")
            # Get list of categories from db for dropdown
            categories = CategoryCRUD.read()
            category_names = [category.category for category in categories]
            # Create dropdown of categories
            category_name = st.selectbox("Category", category_names)
            category_id = next((category.id for category in categories if category.category == category_name), None)
            if category_id:
                if st.form_submit_button("Add Goal"):
                    new_goal = Goal(timestamp=datetime.now(), goal_task=goal_task, is_done=False, duedate=duedate, is_repeat=is_repeat, category_id=category_id)
                    goal_id = GoalCRUD.create(new_goal)
                    st.success(f"Goal added with ID: {goal_id}")
                    # Close modal                
                    st.session_state.show_popover = not st.session_state.show_popover
            else:
                st.warning("No categories found. Please create categories first.")

# Display Goals
st.subheader("Goals")
goals = GoalCRUD.read()
for goal in goals:
    category = categories_collection.find_one({"_id": goal.category_id})
    if category:
        category_name = category["category"]
    else:
        category_name = "General"
    st.write(f"Category: {category_name}")
    st.write(f"Goal Task: {goal.goal_task}")
    st.write(f"Is Done?: {goal.is_done}")
    st.write(f"Due Date: {goal.duedate}")
    st.write(f"Repeat?: {goal.is_repeat}")
    # Edit and Delete buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"Edit {goal.id}", key=f"edit_{goal.id}"):
            # Implement edit functionality
            pass
    with col2:
        if st.button(f"Delete {goal.id}", key=f"delete_{goal.id}"):
            # Implement delete functionality
            pass
