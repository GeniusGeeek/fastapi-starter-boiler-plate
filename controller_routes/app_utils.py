from myutils.master_imports import *

from myutils import app
from fastapi import Form
from fastapi.responses import FileResponse






router = APIRouter()



@router.post("/uploadFile", summary="Upload file along with other form data", tags=["App Utils"])
def file_upload(description: str = Form("write something"),image_file=Depends(app.upload_file), db: Session = Depends(get_db)):
  if (image_file['message'] == "success"):
      return {"message":"Uploaded Successfuly","uploadpath":image_file['file_path'],"description":description}
  else:
      return {"message":"error occured"+ str(image_file)}
  

@router.post("/send_email", summary="Send email", tags=["App Utils"])
def send_mail(request=Depends(app.auth_user_request)):
    response = app.send_mail("mail server","senderemail@mail.com","sender email password","receipient email","message", "subject")
    return {"message": response}
  
  
@router.get("/staticfiles", summary="get and download static files", tags=["App Utils"])
def static_files(filename:str):
    #file_path = os.path.join(path, "uploadedDir/filename.jpg")
    #if os.path.exists(file_path):
        #return FileResponse(file_path, media_type="image/jpeg", filename="mycat.jpg")
    #return {"error": "File not found!"}
    return FileResponse("uploads/"+filename)
  
    
  
  
  
