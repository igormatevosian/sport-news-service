from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from db import services, schemas
from dependencies import get_db

router = APIRouter(prefix="/users",
                   tags=["users"])

limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=schemas.User, responses={400: {"description": "Operation forbidden"}})
@limiter.limit("1000/minute")
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
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
@limiter.limit("1000/minute")
def read_users(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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


@router.get("/{user_id}", response_model=schemas.User, responses={404: {"description": "Not found"}})
@limiter.limit("1000/minute")
def read_user(request: Request, user_id: int, db: Session = Depends(get_db)):
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
@limiter.limit("1000/minute")
def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
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
