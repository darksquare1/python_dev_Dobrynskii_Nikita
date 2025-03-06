from pydantic import BaseModel


class CommentData(BaseModel):
    login: str
    post_header: str
    author_login: str
    comment_count: int
