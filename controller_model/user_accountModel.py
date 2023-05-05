from enum import unique
from unicodedata import category
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models import orm_model, schema_model


def editProfileModel(edit_profileDetails: schema_model.User_EditProfile, db: Session):
  try:
     data = db.query(orm_model.User).filter(orm_model.User.unique_id == edit_profileDetails.unique_id).first()
     if(data is not None):


         data.name = edit_profileDetails.name
         data.username = edit_profileDetails.first_name
         data.email = edit_profileDetails.first_name
         


         db.commit()
         db.refresh(data)
         return{"message": "Successfully Updated Details"}
     else:

         return{"message": "Unique Id not found"}

  except Exception as e:
        return {"message": "Details not Updated, An error occured: "+ str(e)}   
    
    
def delete_user(unique_id,db: Session):
   data = db.query(orm_model.User).filter(orm_model.User.unique_id == unique_id).first()
   if data is None:
           return { "message":"user not found"}

   else:
        db.delete(data)
        db.commit()
        return {"message": "user deleted"}
      
      
      
      
 
def deactivate_accountModel(unique_id, db: Session):
    data = db.query(orm_model.User).filter(
        orm_model.User.unique_id == unique_id).first()
    if data is None:
        return {"message":"user account not found"}

    else:
        data.account_deactiavted = 1
        db.commit()

        db.refresh(data)
        db.close()
        return {"message":"user account deactivated"}

      

def profileDetails(unique_id: str, db: Session):
    data = db.query(orm_model.User).filter(
        orm_model.User.unique_id == unique_id).first()
    return data




