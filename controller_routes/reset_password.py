from app_utils.master_imports import *
from controller_model import signin, signup

from app_utils import utils  






router = APIRouter()


@router.post("/reset-password", summary="user reset password", tags=["User Account"])
def post_data(post_data_in: schema_model.resetPassword, db: Session = Depends(get_db)):
  get_reset_code = signin.login_email(post_data_in.email, db)
  if(get_reset_code is not None):
     reset_code = get_reset_code.email_otp
    
     if(post_data_in.reset_code == reset_code):
         response = signup.reset_password(post_data_in,db)
         return response

     else:
         #raise HTTPException(status_code=400, detail="invalid reset code")
         message= {"message":"invalid reset code"}
         return JSONResponse(status_code=400, content=message)

  
  else:
      #raise HTTPException(status_code=400, detail="Invalid  email")
      message= {"message":"Invalid  email"}
      return JSONResponse(status_code=400, content=message)
      
      
 
@router.post("/change-password", summary="user change password", tags=["User Account"])
def post_data(post_data_in: schema_model.changePassword, db: Session = Depends(get_db), token=Depends(utils.auth_user_request)):

    unique_id = utils.getUserDetails(token['sub'], "unique_id", db)
    if (unique_id == post_data_in.unique_id):
        response = signup.change_password(post_data_in, db)
        return response
    else:
        return {"message": "Invalid user made this request"}
     

      
      
