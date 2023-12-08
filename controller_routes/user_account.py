from app_utils.master_imports import *

from app_utils.utils import auth_user_request, getUserDetails
from controller_model import user_account
from fastapi import Form


router = APIRouter()


@router.post("/edit-profile", summary="edit user profile", tags=["User Account"])
def editProfile(profile_details: schema_model.User_EditProfile, db: Session = Depends(get_db), token=Depends(auth_user_request)):
  unique_id = getUserDetails(token['sub'], "unique_id", db)
  if (unique_id == profile_details.unique_id):
      return user_account.editProfileModel(profile_details, db)
  else:
    return{"message":"Invalid user made this request"}
  
 
@router.delete("/delete-user/{unique_id}", summary="delete user", tags=["User Account"])
def delete_user(unique_id, db: Session = Depends(get_db), token=Depends(auth_user_request)):
  user_unique_id = getUserDetails(token['sub'], "unique_id", db)
  if (str(unique_id) == str(user_unique_id)):
   return user_account.delete_user(unique_id, db)
  else:
     return {"message": "Invalid user made this request"}



@router.post("/deactivate-account", summary="deactivate student account", tags=["User Account"])
def editProfile(user_unique_id: int, db: Session = Depends(get_db), token=Depends(auth_user_request)):
    unique_id = getUserDetails(token['sub'], "unique_id", db)
    if (str(unique_id) == (user_unique_id)):
        return user_account.deactivate_accountModel(unique_id, db)
    else:
        return {"message": "Invalid user made this request"}

    

@router.get("/get-user-details", summary="get user details", tags=["User Account"])
def profileDetails(db: Session = Depends(get_db), token=Depends(auth_user_request)):
    unique_id = getUserDetails(token['sub'], "unique_id", db)
    return user_account.profileDetails(unique_id, db)

