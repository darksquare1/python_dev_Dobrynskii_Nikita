from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from app.db.database import get_db1, get_db2
from app.db.models.authors import User, Post, Comment
from app.db.models.logs import Logs
from app.schemas.comments import CommentData
from app.schemas.general import GeneralData

router = APIRouter()


@router.get('/comments', response_model=list[CommentData])
def get_user_comments(login: str = Query(..., description='Логин пользователя'), db1: Session = Depends(get_db1)):
    user_id = db1.query(User.id).filter(User.login == login).scalar()

    if not user_id:
        raise HTTPException(404, detail=f'User with username {login} not found')

    comments_data = (
        db1.query(
            Comment.post_id,
            Post.header,
            User.login.label('author_login'),
            func.count(Comment.id).label('comment_count')
        )
        .join(Post, Post.id == Comment.post_id)
        .join(User, Post.author_id == User.id)
        .filter(Comment.user_id == user_id)
        .group_by(Comment.post_id, Post.header, User.login)
        .all()
    )

    if not comments_data:
        raise HTTPException(404, detail=f'User with username {login} does not have comments')

    res = [
        CommentData(login=login, post_header=comment.header, author_login=comment.author_login,
                    comment_count=comment.comment_count) for comment in comments_data
    ]

    return res


@router.get('/general', response_model=GeneralData)
def get_general(login: str = Query(..., description='Логин пользователя'), db1: Session = Depends(get_db1),
                db2: Session = Depends(get_db2)):
    user_id = db1.query(User.id).filter(User.login == login).scalar()

    if not user_id:
        raise HTTPException(404, detail=f'User with username {login} not found')

    current_datetime = datetime.now(timezone.utc)

    user_logs = (
        db2.query(
            func.coalesce(func.sum(case((Logs.event_type_id.in_([1]), 1), else_=0)), 0).label('login_count'),
            func.coalesce(func.sum(case((Logs.event_type_id.in_([2]), 1), else_=0)), 0).label('logout_count'),
            func.coalesce(func.sum(case((Logs.event_type_id.in_([3, 4]), 1), else_=0)), 0).label('blog_actions_count'),
        )
        .filter(Logs.user_id == user_id)
        .filter(Logs.date_time <= current_datetime)
        .first()
    )

    return GeneralData(
        date=current_datetime,
        login_count=user_logs.login_count,
        logout_count=user_logs.logout_count,
        blog_actions_count=user_logs.blog_actions_count)
