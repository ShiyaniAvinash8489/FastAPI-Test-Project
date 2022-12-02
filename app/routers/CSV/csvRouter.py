from fastapi import (status,
                     Depends,
                     APIRouter,
                     UploadFile,
                     File,
                     )

# SQLAlchmey ORM
from sqlalchemy.orm import Session

# Import Modules
from app import models

# Import database Settings
from app.db_connection import get_db


# Permission for API
from app.routers.authentication.oAuth2 import authenticated_permission, admin_permission

# CSV
import pandas as pd

# template
from app import main


"""
****************************************************************************************
                                    Router Setting
****************************************************************************************
"""


# Routers Settings
router = APIRouter(
    prefix="/CSV",
    tags=['CSV']
)


"""
****************************************************************************************
                                    CSV File
****************************************************************************************
"""

"""
**************
Upload CSV File
**************
"""


@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(csv_file: UploadFile = File(...), db: Session = Depends(get_db), auth_permission: int = Depends(admin_permission)):

    if csv_file.filename[-4:] != ".csv":
        return {
            "response_code": 400,
            "response_message": "File is not supported."
        }

    df = pd.read_csv(csv_file.file)

    Category_List = []
    for index, row in df.iterrows():
        new_category = models.Category(category_name=row.category_name)

        if not db.query(models.Category).filter(models.Category.category_name == row.category_name).first():
            Category_List.append(new_category)
        continue

    if len(Category_List) > 0:
        db.bulk_save_objects(Category_List)
        db.commit()
        return {"response_code": 200,
                "response_message": f"{len(Category_List)} Record added successfully"
                }
    else:
        return {
            "response_code": 200,
            "response_message": "Record(s) already exists"
        }
