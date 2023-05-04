from myutils.master_imports import *
#from controller_model import custom_model
from myutils.app import auth_user_request, getUserDetails




router = APIRouter()


@router.post("/authenticated_route", summary="A protected/authenticated route")
def post_data(details: schema_model.user_login, db: Session = Depends(get_db), request=Depends(auth_user_request)):
  user_unique_id = getUserDetails(request['sub'], "unique_id", db)
  return {"request_auth_user": request, "inputs": details, "user unique_id detail": user_unique_id}

   #is_admin == 1 to check if user is an admin
  admin_check = getUserDetails(request['sub'], "is_admin", db) 
  if (admin_check == 1):  
    return {"message":"only an admin can access this route","request_auth_user": request, "inputs": details, "user unique_id detail": user_unique_id}

  else:
    return{"message":"Invalid user made this request"}
  
  
