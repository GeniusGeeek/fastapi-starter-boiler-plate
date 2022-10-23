from myutils.master_imports import *

from myutils.app import auth_user_request, upload_file
from fastapi import Form





router = APIRouter()



@router.post("/uploadFile", summary="Upload file along with other data")
def file_upload(description: str = Form(),image_file=Depends(upload_file), db: Session = Depends(get_db), request=Depends(auth_user_request)):
  if (image_file['message'] == "success"):
      return {"message":"Uploaded Successfuly","uploadpath":image_file['file_path']}
  else:
      return {"message":"error occured"+ str(image_file)}
  
  
  
  
