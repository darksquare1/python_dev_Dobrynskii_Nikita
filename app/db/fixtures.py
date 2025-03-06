from sqlalchemy import insert
from app.db.models.logs import SpaceType, EventType, Logs
from app.db.models.authors import User, Blog, Post
from app.db.database import get_db1, get_db2
from app.db.database import engine_db1, engine_db2
from app.db.models.logs import Base as BaseLogs
from app.db.models.authors import Base as BaseAuthors


def create_tables():
    BaseLogs.metadata.create_all(bind=engine_db2)
    BaseAuthors.metadata.create_all(bind=engine_db1)


def add_space_types(db):
    space_types = [
        {'id': 1, 'name': 'global'},
        {'id': 2, 'name': 'blog'},
        {'id': 3, 'name': 'post'}
    ]
    db.execute(insert(SpaceType), space_types)


def add_event_types(db):
    event_types = [
        {'id': 1, 'name': 'login'},
        {'id': 2, 'name': 'logout'},
        {'id': 3, 'name': 'comment'},
        {'id': 4, 'name': 'create_post'},
        {'id': 5, 'name': 'delete_post'}
    ]
    db.execute(insert(EventType), event_types)


def add_users(db):
    users = [
        {'id': 1, 'login': 'user1', 'email': 'user1@example.com'},
        {'id': 2, 'login': 'user2', 'email': 'user2@example.com'},
        {'id': 3, 'login': 'user3', 'email': 'user3@example.com'}
    ]
    db.execute(insert(User), users)


def add_blogs(db):
    blogs = [
        {'id': 1, 'owner_id': 1, 'name': 'Blog 1', 'description': 'This is Blog 1'},
        {'id': 2, 'owner_id': 2, 'name': 'Blog 2', 'description': 'This is Blog 2'}
    ]
    db.execute(insert(Blog), blogs)


def add_posts(db):
    posts = [
        {'id': 1, 'header': 'Post 1', 'text': 'Text of Post 1', 'author_id': 1, 'blog_id': 1},
        {'id': 2, 'header': 'Post 2', 'text': 'Text of Post 2', 'author_id': 2, 'blog_id': 2}
    ]
    db.execute(insert(Post), posts)


def add_logs(db):
    logs = [
        # Логины и логауты (space_type_id = 1, event_type_id = 1 или 2)
        {'id': 1, 'user_id': 1, 'space_type_id': 1, 'event_type_id': 1},
        {'id': 2, 'user_id': 1, 'space_type_id': 1, 'event_type_id': 2},
        {'id': 3, 'user_id': 2, 'space_type_id': 1, 'event_type_id': 1},
        {'id': 4, 'user_id': 2, 'space_type_id': 1, 'event_type_id': 2},
        {'id': 5, 'user_id': 3, 'space_type_id': 1, 'event_type_id': 1},

        # Создание и удаление постов (space_type_id = 2, event_type_id = 3 или 4)
        {'id': 6, 'user_id': 2, 'space_type_id': 2, 'event_type_id': 3},
        {'id': 7, 'user_id': 2, 'space_type_id': 2, 'event_type_id': 4},
        {'id': 8, 'user_id': 1, 'space_type_id': 2, 'event_type_id': 3},
        {'id': 9, 'user_id': 1, 'space_type_id': 2, 'event_type_id': 4},

        # Комментарии к постам (space_type_id = 3, event_type_id = 5)
        {'id': 10, 'user_id': 3, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 11, 'user_id': 3, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 12, 'user_id': 1, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 13, 'user_id': 2, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 14, 'user_id': 2, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 15, 'user_id': 1, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 16, 'user_id': 3, 'space_type_id': 3, 'event_type_id': 5},
    ]

    db.execute(insert(Logs), logs)


def load_fixtures():
    """Функция для создания таблиц и загрузки данных в обе базы данных"""
    create_tables()

    with next(get_db1()) as db1:
        add_users(db1)
        add_blogs(db1)
        add_posts(db1)
        db1.commit()

    with next(get_db2()) as db2:
        add_space_types(db2)
        add_event_types(db2)
        add_logs(db2)
        db2.commit()


if __name__ == '__main__':
    load_fixtures()
