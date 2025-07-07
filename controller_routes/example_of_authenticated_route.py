from app_utils.master_imports import *
#from controller_model import custom_model
from app_utils.utils import auth_user_request, getUserDetails




router = APIRouter()


@router.post("/authenticated-route", summary="A protected/authenticated route")
def post_data(details: schema_model.user_login, db: Session = Depends(get_db), token=Depends(auth_user_request)):
  user_unique_id = getUserDetails(token['sub'], "unique_id", db)
  return {"request_auth_user": token, "inputs": details, "user unique_id detail": user_unique_id}

   #is_admin == 1 to check if user is an admin
  admin_check = getUserDetails(token['sub'], "is_admin", db) 
  if (admin_check == 1):  
    return {"message":"only an admin can access this route","request_auth_user": token, "inputs": details, "user unique_id detail": user_unique_id}

  else:
    return{"message":"Invalid user made this request"}
  
 