from myutils.master_imports import *
from controller_model import signin, signup

from myutils import app  






router = APIRouter()

@router.post("/reset_password", summary="user reset password")
def post_data(post_data_in: schema_model.resetPassword, db: Session = Depends(get_db)):
  check_email = signin.login_email(post_data_in.email, db)
  reset_code = check_email.account_hash

  if(check_email):
    if(post_data_in.reset_code == reset_code):
      response = signup.reset_password(post_data_in,db)
      return response

    else:
      raise HTTPException(status_code=400, detail="invalid reset code")

  else:  
    raise HTTPException(status_code=400, detail="email does not exist")
