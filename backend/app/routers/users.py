from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import schemas, services
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])



@router.post(
    "/",
    response_model=schemas.User,
    responses={400: {"description": "Operation forbidden"}},
)
def create_user(
     user: schemas.UserCreate, db: Session = Depends(get_db)
):
    """
    Create a new user.

    - **user**: Details of the user to be created.
    - **db**: Database session dependency.

    Returns:
    - **201 Created**: User created successfully.
    - **400 Bad Request**: If user with provided email already exists.
    """
    user_service = services.UserService(db)
    return user_service.create_user(user)


@router.get("/", response_model=list[schemas.User])

def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve a list of users.

    - **skip**: Number of users to skip.
    - **limit**: Maximum number of users to return.
    - **db**: Database session dependency.

    Returns:
    - List of users.
    """
    user_service = services.UserService(db)
    return user_service.get_users(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=schemas.User,
    responses={404: {"description": "Not found"}},
)

def read_user( user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve user by ID.

    - **user_id**: ID of the user to retrieve.
    - **db**: Database session dependency.

    Returns:
    - **200 OK**: User retrieved successfully.
    - **404 Not Found**: If user with provided ID does not exist.
    """
    user_service = services.UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=bool)
def delete_user( user_id: int, db: Session = Depends(get_db)):
    """
    Delete user by ID.

    - **user_id**: ID of the user to delete.
    - **db**: Database session dependency.

    Returns:
    - **True**: User deleted successfully.
    - **False**: If user with provided ID does not exist.
    """
    user_service = services.UserService(db)
    result = user_service.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
