from myutils.master_imports import *

from myutils.app import auth_user_request




router = APIRouter()


@router.post("/protected_route", summary="A protected route")
def post_data(details: schema_model.user_login, db: Session = Depends(get_db), request=Depends(auth_user_request)):
  return {"request_auth_user": request, "inputs": details}
  