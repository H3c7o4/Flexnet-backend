from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Score
from .. import schemas
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/scores',
    tags=['Scores']
)

@router.post('/', response_model=schemas.ShowScore, status_code=status.HTTP_201_CREATED)
async def rate_film(request: schemas.Score, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    new_score = Score(user_id=request.user_id, film_id=request.film_id, value=request.value)
    conditions = [
        Score.film_id == request.film_id,
        Score.user_id == request.user_id
    ]
    score = db.query(Score).filter(and_(*conditions)).first()

    if score:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Score with user\'s id {request.user_id} already exist')
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score

@router.put('/update', response_model=schemas.ShowScore, status_code=status.HTTP_202_ACCEPTED)
async def update_rating(request: schemas.Score, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    conditions = [
        Score.film_id == request.film_id,
        Score.user_id == request.user_id
    ]
    score = db.query(Score).filter(and_(*conditions)).first()

    if not score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Score with the id {score.id} is not available')
    score.user_id = request.user_id
    score.film_id = request.film_id
    score.value = request.value
    db.commit()

    return schemas.ShowScore(user_id=Score.user_id, film_id=Score.film_id, value=Score.value)
