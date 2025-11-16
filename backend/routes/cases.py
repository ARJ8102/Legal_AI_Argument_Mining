from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# ---- Mongo Setup ----
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_pipeline"]
cases_collection = db["cases"]


# Helper to convert Mongo ObjectId
def serialize_case(case):
    return {
        "doc_id": str(case["_id"]),
        "filename": case.get("filename", ""),
        "raw_text": case.get("raw_text", ""),
        "entities": case.get("entities", []),
        "sentences": case.get("sentences", []),
        "classifications": case.get("classifications", [])
    }



# ---------------------------
# 1. GET ALL CASES
# ---------------------------
@router.get("/cases")
def get_all_cases():
    cases = list(cases_collection.find({}, {
        "_id": 1,
        "filename": 1,
        "created_at": 1,
        "entities": 1,
        "classifications": 1
    }))

    return {
        "status": "success",
        "cases": [serialize_case(c) for c in cases]
    }


# ---------------------------
# 2. GET ONE CASE BY ID
# ---------------------------
@router.get("/cases/{case_id}")
def get_case(case_id: str):
    case = cases_collection.find_one({"_id": case_id})

    if not case:
        raise HTTPException(404, "Case not found")

    return {
        "status": "success",
        "case": serialize_case(case)
    }


# ---------------------------
# 3. DELETE ONE CASE
# ---------------------------
@router.delete("/cases/{case_id}")
def delete_case(case_id: str):

    result = cases_collection.delete_one({"_id": case_id})

    if result.deleted_count == 0:
        raise HTTPException(404, "Case not found")

    return {
        "status": "success",
        "message": f"Case {case_id} deleted."
    }


# ---------------------------
# 4. DELETE ALL CASES
# ---------------------------
@router.delete("/cases")
def delete_all_cases():
    count = cases_collection.count_documents({})
    cases_collection.delete_many({})

    return {
        "status": "success",
        "message": f"Deleted {count} cases."
    }


# ---------------------------
# 5. UPDATE CASE SUMMARY (optional)
# ---------------------------
@router.put("/cases/{case_id}/summary")
def update_summary(case_id: str, summary: dict):

    result = cases_collection.update_one(
        {"_id": case_id},
        {"$set": {"summary": summary.get("summary")}}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Case not found")

    return {
        "status": "success",
        "message": "Summary updated"
    }
