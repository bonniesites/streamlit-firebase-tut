from mods.base import *
from mods.utils import *

# Define Pydantic model
class UserForm(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=20)
    email: EmailStr
    age: int

# Create Streamlit form
with st.form("user_form"):
    username = st.text_input("Username", max_chars=20)
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, format="%d")
    submitted = st.form_submit_button("Submit")

# Validate input with Pydantic
if submitted:
    try:
        form_data = UserForm(username=username, email=email, age=age)
        st.success("Validation successful!")
        st.json(form_data.dict())
    except ValidationError as e:
        for error in e.errors():
            st.error(f"{error['loc'][0]}: {error['msg']}")
