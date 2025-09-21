from pymongo import MongoClient

# Connect to MongoDB service running locally
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]

# List all collections in this database
collections = db.list_collection_names()
print("Collections in legal_pipeline:", collections)

# Optional: create a test document
test_doc = {"_id": "test_doc", "text": "Hello MongoDB!"}
db.documents.insert_one(test_doc)
print("Inserted test document.")
