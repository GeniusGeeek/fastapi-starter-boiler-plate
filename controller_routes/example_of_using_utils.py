from app_utils.master_imports import *

from app_utils import utils
from fastapi import Form, File, UploadFile
from fastapi.responses import FileResponse
from typing import Optional







router = APIRouter()



@router.post("/upload-file", summary="Upload file along with other form data", tags=["App Utils"])
def file_upload(description: str = Form("write default content or leave blank without quotes"),image_file=Depends(utils.upload_file), db: Session = Depends(get_db)):
  if (image_file['message'] == "success"):
      return {"message":"Uploaded Successfuly","uploadpath":image_file['file_path'],"description":description}
  else:
      return {"message":"error occured"+ str(image_file)}
    

@router.post("/upload-optional-file", summary="Upload Optional file", tags=["App Utils"])
def file_upload(description: str = Form(),image_file=Depends(utils.optional_upload_file), db: Session = Depends(get_db)):
    if image_file is not None:

        if (image_file['message'] == "success"):
            return {"message": "Uploaded Successfuly", "uploadpath": image_file['file_path'], "description": "description"}
        else:
            return {"message": "error occured" + str(image_file)}

    else:

        return {"message": description}

    
@router.post("/upload/optional/formdata", summary="Upload optinal file along with other optional form data", tags=["App Utils"])
def file_upload(description: Optional[str] = Form(None),image_file: UploadFile = File(None), db: Session = Depends(get_db)):
   if image_file:

        image_file_data = utils.upload_file(image_file)
        if (image_file_data['message'] == "success"):
            return {"message":"Uploaded Successfuly","uploadpath":image_file['file_path'],"description":description}
        else:
          return {"message":"error occured"+ str(image_file)}

   else:
       
        return {"message": description}
      
      
@router.post("/upload-multiple-files", summary="Upload fmultiple files", tags=["App Utils"])
def file_upload(image_file=Depends(utils.upload_multiple_files), db: Session = Depends(get_db)):
  if (image_file['message'] == "success"):
      return {"message":"Uploaded Successfuly","uploadpath":image_file['file_paths']}
  else:
      return {"message":"error occured"+ str(image_file)}
  
  

@router.post("/send-email", summary="Send email", tags=["App Utils"])
def send_mail(token=Depends(utils.auth_user_request)):
    #email details are imported from master_imports.py
    response = utils.send_mail(email_host,email_address,email_password,"receipient email","message", "subject",email_port)
    return {"message": response}
  
  
@router.get("/static-files", summary="get and download static files", tags=["App Utils"])
def static_files(filename:str):

    file_path = "uploads/"+filename
    if os.path.exists(file_path):
        #return FileResponse(file_path, media_type="image/jpeg", filename="mycat.jpg")
        return FileResponse("uploads/"+filename)
    else:
      return {"error": "File not found!"}
    
  
    
  
  
  
