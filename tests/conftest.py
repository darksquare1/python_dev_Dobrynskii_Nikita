import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models.authors import Base as BaseAuthors
from app.db.models.logs import Base as BaseLogs
from app.db.models.authors import User, Blog, Post, Comment
from app.db.models.logs import SpaceType, EventType, Logs


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    DB1_URL = 'sqlite:///test_authors_database.db'
    DB2_URL = 'sqlite:///test_logs_database.db'

    test_engine_db1 = create_engine(DB1_URL)
    test_engine_db2 = create_engine(DB2_URL)

    BaseAuthors.metadata.create_all(test_engine_db1)
    BaseLogs.metadata.create_all(test_engine_db2)

    users = [
        {'id': 1, 'login': 'testuser1', 'email': 'testuser1@example.com'},
        {'id': 2, 'login': 'testuser2', 'email': 'testuser2@example.com'},
        {'id': 3, 'login': 'testuser3', 'email': 'testuser3@example.com'},
        {'id': 4, 'login': 'testuser4', 'email': 'testuser4@example.com'}
    ]
    event_types = [
        {'id': 1, 'name': 'login'},
        {'id': 2, 'name': 'logout'},
        {'id': 3, 'name': 'create_post'},
        {'id': 4, 'name': 'delete_post'},
        {'id': 5, 'name': 'comment'}
    ]
    space_types = [
        {'id': 1, 'name': 'global'},
        {'id': 2, 'name': 'blog'},
        {'id': 3, 'name': 'post'}
    ]
    comments = [
        {'id': 1, 'post_id': 1, 'user_id': 2, 'text': 'Test comment'},
        {'id': 2, 'post_id': 1, 'user_id': 2, 'text': 'Second test comment'},
        {'id': 3, 'post_id': 2, 'user_id': 3, 'text': 'Third test comment'},
        {'id': 4, 'post_id': 1, 'user_id': 3, 'text': 'Fourth test comment'}
    ]
    blogs = [
        {'id': 1, 'owner_id': 1, 'name': 'Test Blog', 'description': 'Test'},
        {'id': 2, 'owner_id': 2, 'name': 'Test Blog 2', 'description': 'Test2'}
    ]
    posts = [
        {'id': 1, 'header': 'Test Post', 'text': 'Test content', 'author_id': 1, 'blog_id': 1},
        {'id': 2, 'header': 'Test Post 2', 'text': 'Test content 2', 'author_id': 2, 'blog_id': 2}
    ]
    logs = [
        {'id': 1, 'user_id': 1, 'space_type_id': 1, 'event_type_id': 1},
        {'id': 2, 'user_id': 1, 'space_type_id': 1, 'event_type_id': 2},
        {'id': 3, 'user_id': 2, 'space_type_id': 2, 'event_type_id': 3},
        {'id': 4, 'user_id': 2, 'space_type_id': 2, 'event_type_id': 3},
        {'id': 5, 'user_id': 2, 'space_type_id': 2, 'event_type_id': 4},
        {'id': 6, 'user_id': 3, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 7, 'user_id': 3, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 8, 'user_id': 2, 'space_type_id': 3, 'event_type_id': 5},
        {'id': 9, 'user_id': 2, 'space_type_id': 3, 'event_type_id': 5},
    ]

    with sessionmaker(bind=test_engine_db1)() as db1:
        for user in users:
            db1.add(User(**user))
        for blog in blogs:
            db1.add(Blog(**blog))
        for post in posts:
            db1.add(Post(**post))
        for comment in comments:
            db1.add(Comment(**comment))
        db1.commit()

    with sessionmaker(bind=test_engine_db2)() as db2:
        for space in space_types:
            db2.add(SpaceType(**space))
        for event in event_types:
            db2.add(EventType(**event))
        for log in logs:
            db2.add(Logs(**log))
        db2.commit()

    yield

    BaseAuthors.metadata.drop_all(test_engine_db1)
    BaseLogs.metadata.drop_all(test_engine_db2)
