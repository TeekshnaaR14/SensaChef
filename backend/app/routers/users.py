from fastapi import APIRouter
from app.database import supabase
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi import HTTPException
router = APIRouter()
class userModel(BaseModel):
    name: str
    email: str
    username: str
    password: str
    creationDate: datetime
    
@router.get("/users", tags=["users"])
async def read_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data

@router.get("/recipes", tags=["recipes"])
async def get_all_recipes():
    response = supabase.table("recipes").select("*").execute()
    return response.data

# --------------------------------
# API endpoints for recipes:
@router.get("/recipes/{recipe_id}", tags=["recipes"])
async def get_recipe(recipe_id: int):
    response = supabase.table("recipes").select("*").eq("id", recipe_id).execute()
    return response.data[0]

@router.get("/recipes/{recipe_id}/steps", tags=["recipes"])
async def get_recipe_steps(recipe_id: int):
    try:
        recipe_exists = supabase.table("steps").select("id").eq("id", recipe_id).execute()
        if not recipe_exists.data:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        response = supabase.table("steps").select("*").eq("recipe_id", recipe_id).order("step_number").execute()
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # query = supabase.table("steps").select("*").eq("recipe_id", recipe_id)
    # if step_number:
    #     query = query.eq("step_number", step_number)
    # response = query.execute()
    # return response.data
# ---------------------------------

@router.post("/users", tags=["users"])
async def create_user(user: userModel):
    response = supabase.table("users").insert({"name": user.name, "email": user.email, "username": user.username, "password": user.password, "creationDate": (datetime.now(timezone.utc)).isoformat()}).execute()
    return response.data

@router.post("/users/recipes", tags=["users"])
async def user_recipes(user_id: str):
    response = supabase.table("recipes").select("*, steps(*)").eq("user_id", user_id).execute()
    return response.data

@router.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: str, user: userModel):
    response = supabase.table("users").update({
        "name": user.name,
        "email": user.email
    }).eq("user_id", user_id).execute()
    return response.data

@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: str):
    response = supabase.table("users").delete().eq("user_id", user_id).execute()
    return response.data
