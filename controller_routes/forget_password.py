from myutils.master_imports import *
from controller_model import  signin
from myutils import app  
import random






router = APIRouter()


@router.post("/forget_password", summary="user forget password", tags=["User Account"])
def post_data(post_data_in: schema_model.forgotPassword, db: Session = Depends(get_db)):
  check_email = signin.forgotPassModel(post_data_in.email, db)
 

  if(check_email):
       return check_email
    
  else:  
       raise HTTPException(status_code=400, detail="an error occured")
