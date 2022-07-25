from controller_model import signup
from myutils.master_imports import *
from fastapi import FastAPI






router = APIRouter()




@router.post('/signup')
def register(user: schema_model.User, db: Session = Depends(get_db)):
    create_user = signup.check_email_exist(db, user.email)
    if(create_user):
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        return signup.create_user(user, db)
