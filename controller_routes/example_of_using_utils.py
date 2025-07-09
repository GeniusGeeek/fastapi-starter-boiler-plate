from app_utils.master_imports import *

from app_utils import utils
from fastapi import Form, File, UploadFile
from fastapi.responses import FileResponse
from typing import Optional
from pathlib import Path


router = APIRouter()


@router.post("/upload-file", summary="Upload file along with other form data", tags=["App Utils"])
def file_upload(description: str = Form("write default content or leave blank without quotes"), image_file=Depends(utils.upload_file), db: Session = Depends(get_db)):
    if (image_file['message'] == "success"):
        return {"message": "Uploaded Successfuly", "uploadpath": image_file['file_path'], "description": description}
    else:
        return {"message": "error occured" + str(image_file)}


@router.post("/upload-optional-file", summary="Upload Optional file", tags=["App Utils"])
def file_upload(description: str = Form(), image_file=Depends(utils.optional_upload_file), db: Session = Depends(get_db)):
    if image_file is not None:

        if (image_file['message'] == "success"):
            return {"message": "Uploaded Successfuly", "uploadpath": image_file['file_path'], "description": "description"}
        else:
            return {"message": "error occured" + str(image_file)}

    else:

        return {"message": description}


@router.post("/upload/optional/formdata", summary="Upload optinal file along with other optional form data", tags=["App Utils"])
def file_upload(description: Optional[str] = Form(None), image_file: UploadFile = File(None), db: Session = Depends(get_db)):
    if image_file:

        image_file_data = utils.upload_file(image_file)
        if (image_file_data['message'] == "success"):
            return {"message": "Uploaded Successfuly", "uploadpath": image_file['file_path'], "description": description}
        else:
            return {"message": "error occured" + str(image_file)}

    else:

        return {"message": description}


@router.post("/upload-multiple-files", summary="Upload fmultiple files", tags=["App Utils"])
def file_upload(image_file=Depends(utils.upload_multiple_files), db: Session = Depends(get_db)):
    if (image_file['message'] == "success"):
        return {"message": "Uploaded Successfuly", "uploadpath": image_file['file_paths']}
    else:
        return {"message": "error occured" + str(image_file)}


@router.post("/send-email", summary="Send email", tags=["App Utils"])
async def send_mail(file_attachment: UploadFile | None = File(None)):
    # email details are imported from master_imports.py
    attachments = []
    file_path = None
    # note any of these file path sytnax will work when used below

    # file_path = Path("uploads/uploadedfile.txt")
    # file_path = [
    #     Path("uploads/uploadedfile.txt"),
    #     Path("uploads/uploadedfile2.txt")
    # ]
    # file_path = ["uploads/uploadedfile.txt", "uploads/uploadedfile2.txt"]

    message_body = """Thank you for your interest in using FASTAPI boiler plate<br>
    Created By Gracious Emmanuel
    """

    if file_path is not None:
        # Ensure it's a list if you have multiple paths
        if isinstance(file_path, list):
            attachments.extend(file_path)
        else:
            attachments.append(file_path)

    if file_attachment:
        # read the bytes once
        file_attachment_bytes = await file_attachment.read()
        attachments.append((file_attachment.filename, file_attachment_bytes))
    response = utils.send_mail(email_host, email_address, email_password,

                               "graciousemmanuel52@gmail.com,rewodtechnologies@gmail.com", message_body, "Welcome to FASTAPI Boiler Plate", email_port, attachments)
    return {"message": response}


@router.get("/static-files", summary="get and download static files", tags=["App Utils"])
def static_files(filename: str):

    file_path = "uploads/"+filename
    if os.path.exists(file_path):
        # return FileResponse(file_path, media_type="image/jpeg", filename="mycat.jpg")
        return FileResponse("uploads/"+filename)
    else:
        return {"error": "File not found!"}
