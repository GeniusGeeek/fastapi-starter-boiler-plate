from myutils.master_imports import *

from myutils import app
from fastapi import Form





router = APIRouter()



@router.post("/uploadFile", summary="Upload file along with other form data", tags=["App Utils"])
def file_upload(description: str = Form(),image_file=Depends(app.upload_file), db: Session = Depends(get_db), request=Depends(app.auth_user_request)):
  if (image_file['message'] == "success"):
      return {"message":"Uploaded Successfuly","uploadpath":image_file['file_path']}
  else:
      return {"message":"error occured"+ str(image_file)}
  

@router.post("/send_email", summary="Send email", tags=["App Utils"])
def send_mail(request=Depends(app.auth_user_request)):
    response = app.send_mail("mail server","senderemail@mail.com","sender email password","receipient email","message", "subject")
    return {"message": response}
  
    
  
  
  
