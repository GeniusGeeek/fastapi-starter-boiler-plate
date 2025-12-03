from app_utils.master_imports import *
# from controller_model import custom_model
from app_utils.utils import auth_user_request, getUserDetails


router = APIRouter()


@router.post("/load_result", summary="load result with pagination, starting first page with 1")
def loadresult_withpagination(search_data: str, page: int, db: Session = Depends(get_db)):

    def loadmore_more(search_data: str, page: int, db: Session):
        searchterm = "%{}%".format(search_data)
        page = int(page)
        if (page < 1):
            page = 1
        offset = (page - 1) * 20
        result = db.query(orm_model.User).filter(orm_model.User.name.like(
            searchterm)).order_by(orm_model.User.id.desc()).offset(offset).limit(20).all()

        return result
    if (page is not None):
        data = loadmore_more(search_data, page, db)

        if (data is None or len(data) == 0):
            return {"message": "No more results"}
        else:
            return data


@router.post("/load_result_with_data", summary="load result with pagination data, starting first page with 1")
def loadresult_withpagination_data(search_data: str, page: int, db: Session = Depends(get_db)):

    def loadmore_more_with_pagination_data(search_data: str, page: int, db: Session):
        searchterm = "%{}%".format(search_data)

        try:
            page = int(page)
        except:
            page = 1

        if page < 1:
            page = 1

        limit = 50
        offset = (page - 1) * limit

        query = db.query(
            orm_model.User
        ).filter(
            orm_model.User.name.like(
                searchterm)
        )

        # Count total records
        total_records = query.count()

        # Calculate pages
        total_pages = (total_records + limit - 1) // limit  # ceiling division

        # Fetch paginated results
        results = query.order_by(orm_model.User.id.desc()).offset(
            offset).limit(limit).all()

        # Convert results to list of dicts
        # data = []
        # for r in results:
        #     data.append({
        #         "id": r.id,
        #         "employee_unique_id": r.employee_unique_id,
        #         "date": r.date,
        #         "time_in": r.time_in,
        #         "time_out": r.time_out,
        #         "project_site_id": r.project_site_id
        #     })

        return {
            "current_page": page,
            "page_size": limit,
            "total_pages": total_pages,
            "total_records": total_records,
            "data": results
        }

    if (page is not None):
        data = loadmore_more_with_pagination_data(search_data, page, db)

        if (data is None or len(data) == 0):
            return {"message": "No more results"}
        else:
            return data
