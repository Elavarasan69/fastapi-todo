from fastapi import FastAPI, APIRouter, HTTPException 
from config import collection
from Database.schemas import all_tasks
from Database.models import Todo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI()
router = APIRouter()

@router.get("/display")
async def get_all_todos():
    data = collection.find()
    return all_tasks(data)

@router.post("/add")
async def create_task(newTask: Todo):
    try:
        response = collection.insert_one(dict(newTask))
        return {"status_code":200, "id":str(response.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail={e})
    
@router.put("/update/{task_id}")
async def update_task(task_id:str, updated_task:Todo):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id":id})
        if not existing_doc:
            return HTTPException(status_code=404, detail={"Task does not exist"})
        updated_task.updated_at = datetime.timestamp(datetime.now())
        response = collection.update_one({"_id":id},{"$set":dict(updated_task)})
        return {"status_code":200, "message":"Task updated successfully"}
    except Exception as e:        
        return HTTPException(status_code=500, detail={e})

@router.delete("/delete/{task_id}")
async def delete_task(task_id:str):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id":id})
        if not existing_doc:
            return HTTPException(status_code=404, detail={"Task does not exist"})
        response = collection.delete_one({"_id":id})
        return {"status_code":200, "message":"Task deleted successfully"}
    except Exception as e:        
        return HTTPException(status_code=500, detail={e})

app.include_router(router)