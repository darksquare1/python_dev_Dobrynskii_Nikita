from datetime import datetime
from pydantic import BaseModel


class GeneralData(BaseModel):
    date: datetime
    login_count: int
    logout_count: int
    blog_actions_count: int