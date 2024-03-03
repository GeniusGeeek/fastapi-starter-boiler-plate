from app_utils.master_imports import *
#from controller_model import custom_model
from app_utils.utils import auth_user_request, getUserDetails




router = APIRouter()


@router.post("/load_result", summary="load result with pagination, starting first page with 1")
def loadresult_withpagination(search_data: str, page:int, db: Session = Depends(get_db)):
    
    def loadmore_more(search_data: str, page:int, db: Session):
        searchterm = "%{}%".format(search_data)
        page = int(page)
        offset = (page - 1) * 20
        result = db.query(orm_model.User).filter(orm_model.User.name.like(searchterm)).order_by(orm_model.User.id.desc()).offset(offset).limit(20).all()
       
        return result
    if (page is not None):
        data = loadmore_more(search_data,page, db)

        if (data is None or len(data) == 0):
            return {"message": "No more results"}
        else:
            return data
