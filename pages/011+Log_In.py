SIDEBAR = 'collapsed'
PAGE_HEADER = 'Login'
PAGE_SUBHEADER = ''

from mods.data_processing import *
from mods.models import LoginRequest

PAGE_HEADER = 'Authentication'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'Login'


from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

roles_collection = REDDIT_DB.roles

# Authenticate user
def authenticate(email: str, password: str) -> dict:
    user_data = REDDIT_USERS.find_one({"email": email})
    if user_data and bcrypt.verify(password, user_data["password"]):
        return user_data
    return None

# Streamlit UI for user login
def login_page():
    st.subheader("Login")
    login_form = sp.pydantic_form(key="login_form", model=LoginRequest)
    if login_form:
        user = authenticate(login_form.email, login_form.password)
        if user:
            st.success("Login successful")
            return user
        else:
            st.error("Invalid email or password")
    return None

# Streamlit UI for user dashboard
def user_dashboard(user_data):
    st.subheader("User Dashboard")
    st.write(f"Name: {user_data['name']}")
    st.write(f"Email: {user_data['email']}")
    st.write(f"Role: {user_data['role_id']}")

    # Form to update user information
    st.subheader("Update User Information")
    update_form = sp.pydantic_form(UserUpdate)
    if update_form:
        update_data = update_form.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = bcrypt.hash(update_data["password"])
        REDDIT_USERS.update_one({"email": user_data["email"]}, {"$set": update_data})
        st.success("User information updated successfully")

# Main function
def main():

    # Display login page
    user_data = login_page()

    # If user is authenticated, display user dashboard
    if user_data:
        user_dashboard(user_data)

if __name__ == "__main__":
    main()
