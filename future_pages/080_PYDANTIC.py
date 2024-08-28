import streamlit as st

from mods.data_processing import *


# Set up MongoDB connection
CONN = MongoClient('localhost:27017')
# CONN = MongoClient(st.secrets.mongo.conn_string)
db = CONN["goals"]
collection = db["goals_list"]

# Pydantic model for item
class Item(BaseModel):
    name: str
    description: str
    quantity: int

# CRUD operations for items
class ItemCRUD:
    @staticmethod
    def create(item: Item) -> str:
        result = collection.insert_one(item.dict())
        return str(result.inserted_id)

    @staticmethod
    def read() -> list[Item]:
        items = collection.find()
        return [Item(**item) for item in items]

    @staticmethod
    def update(item_id: str, item: Item) -> int:
        result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
        return result.modified_count

    @staticmethod
    def delete(item_id: str) -> int:
        result = collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count

# Streamlit UI
st.title("CRUD App")

# Create
st.subheader("Create Item")
with st.form(key="create_form"):
    item = sp.pydantic_form(Item)
    if st.form_submit_button("Create"):
        item_id = ItemCRUD.create(item)
        st.success(f"Item created with ID: {item_id}")

# Read
st.subheader("View Items")
items = ItemCRUD.read()
for item in items:
    st.write(f"ID: {item.id}, Name: {item.name}, Description: {item.description}, Quantity: {item.quantity}")

# Update
st.subheader("Update Item")
with st.form(key="update_form"):
    item_id = st.text_input("Enter Item ID")
    if st.form_submit_button("Fetch"):
        item_to_update = next((item for item in items if str(item.id) == item_id), None)
        if item_to_update:
            new_item = sp.pydantic_form(Item, obj=item_to_update)
            if st.form_submit_button("Update"):
                updated_count = ItemCRUD.update(item_id, new_item)
                if updated_count > 0:
                    st.success("Item updated successfully")
                else:
                    st.error("Failed to update item")

# Delete
st.subheader("Delete Item")
item_id = st.text_input("Enter Item ID")
if st.button("Delete"):
    deleted_count = ItemCRUD.delete(item_id)
    if deleted_count > 0:
        st.success("Item deleted successfully")
    else:
        st.error("Failed to delete item")
