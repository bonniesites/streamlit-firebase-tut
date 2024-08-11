import streamlit as st
from pydantic import *
#import streamlit_pydantic as sp
from passlib.hash import bcrypt
from typing import Optional
from pydantic_settings import BaseSettings
import streamlit as st
from pydantic import *
#import streamlit_pydantic as sp
from passlib.hash import bcrypt
from typing import Optional
from pydantic_settings import BaseSettings

# Define Pydantic model
class UserForm(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    age: int
    
# Pydantic model for user
class User(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    role_id: str

# Pydantic model for user login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Pydantic model for user update
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str] = Field(min_length=8)
    role_id: Optional[str]

# # Create Streamlit form
# with st.form("user_form"):
#     username = st.text_input("Username", max_chars=20)
#     email = st.text_input("Email")
#     age = st.number_input("Age", min_value=0, format="%d")
#     submitted = st.form_submit_button("Submit")

# # Validate input with Pydantic
# if submitted:
#     try:
#         form_data = UserForm(username=username, email=email, age=age)
#         st.success("Validation successful!")
#         st.json(form_data.dict())
#     except ValidationError as e:
#         for error in e.errors():
#             st.error(f"{error['loc'][0]}: {error['msg']}")
# # Validate input with Pydantic
# if submitted:
#     try:
#         form_data = UserForm(username=username, email=email, age=age)
#         st.success("Validation successful!")
#         st.json(form_data.dict())
#     except ValidationError as e:
#         for error in e.errors():
#             st.error(f"{error['loc'][0]}: {error['msg']}")
