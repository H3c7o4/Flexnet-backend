from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


from .. import schemas
from ..database import get_db
from ..hashing import Hash
from ..models import User
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/', status_code=status.HTTP_200_OK)
async def show_users(
        skip: int = 0,
        limit: int = 2,
        db: Session = Depends(get_db),
        get_current_user: schemas.User = Depends(get_current_user)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get('/{id}', response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
async def get_user(id: int,
                   db: Session = Depends(get_db),
                   get_current_user: schemas.User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    return user

@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User,
                      db: Session = Depends(get_db)):
    new_user = User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Email {new_user.email} already registered')
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put('/{id}', response_model=schemas.ShowUser, status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: int,
                      request: schemas.User,
                      db: Session = Depends(get_db),
                      get_current_user: schemas.User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id of {id} is not available')
    user.email = request.email
    user.password = request.password
    user.name = request.name
    db.commit()
    return schemas.ShowUser(id=user.id, name=user.name, email=user.email)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int,
                      db: Session = Depends(get_db),
                      get_current_user: schemas.User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id of {id} is not available')
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Delete User': 'Done'}