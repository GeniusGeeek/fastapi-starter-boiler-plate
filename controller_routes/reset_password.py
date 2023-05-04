from myutils.master_imports import *
from controller_model import signin, signup

from myutils import app  






router = APIRouter()


@router.post("/reset_password", summary="user reset password", tags=["User Account"])
def post_data(post_data_in: schema_model.resetPassword, db: Session = Depends(get_db)):
  get_reset_code = signin.login_email(post_data_in.email, db)
  if(get_reset_code is not None):
     reset_code = get_reset_code.email_otp
    
     if(post_data_in.reset_code == reset_code):
         response = signup.reset_password(post_data_in,db)
         return response

     else:
         raise HTTPException(status_code=400, detail="invalid reset code")

  
  else:
      raise HTTPException(status_code=400, detail="Invalid  email")
      
      
 
@router.post("/change_password", summary="user change password", tags=["User Account"])
def post_data(post_data_in: schema_model.changePassword, db: Session = Depends(get_db), request=Depends(app.auth_user_request)):

    unique_id = app.getUserDetails(request['sub'], "unique_id", db)
    if (unique_id == post_data_in.unique_id):
        response = signup.change_password(post_data_in, db)
        return response
    else:
        return {"message": "Invalid user made this request"}
     

      
      
