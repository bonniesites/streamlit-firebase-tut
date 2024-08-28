from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Access the goals database and the collection
goals_db = client['goals']
goals_collection = goals_db['goals_list']  # Replace 'goals_list' with your collection name

# Access the options database and the collection
charlie_db = client['charlie']
charlie_collection = charlie_db['charlie_list']  # Replace 'options_list' with your desired collection name

# Find all documents in the goals collection with 'option' in the 'category' field
charlie_documents = list(goals_collection.find({ "category": { "$regex": "charlie", "$options": "i" } }))

# Insert the found documents into the options collection
print(f'Number of documents in goals_list: {len(list(charlie_documents))}')
if len(charlie_documents) > 0:
    charlie_collection.insert_many(charlie_documents)

# Delete the original documents from the goals collection
goals_collection.delete_many({ "category": { "$regex": "charlie", "$options": "i" } })

# Close the connection
client.close()

print("Documents with 'charlie' in 'category' field have been copied and deleted.")
