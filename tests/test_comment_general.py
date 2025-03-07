import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import get_db1, get_db2
from main import app


@pytest.fixture(scope="module")
def client():
    """Фикстура для подмены баз данных на тестовые"""

    def get_test_db1():
        test_engine = create_engine('sqlite:///test_authors_database.db')
        TestSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=test_engine
        )
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_test_db2():
        test_engine = create_engine('sqlite:///test_logs_database.db')
        TestSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=test_engine
        )
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db1] = get_test_db1
    app.dependency_overrides[get_db2] = get_test_db2

    with TestClient(app) as c:
        yield c


def test_general_data(client):
    """Проверка общей статистики для testuser1"""
    response = client.get('/api/general?login=testuser1')
    assert response.status_code == 200
    data = response.json()
    assert data['login_count'] == 1
    assert data['logout_count'] == 1
    assert data['blog_actions_count'] == 0
    assert 'date' in data


def test_nonexistent_user(client):
    """Проверка ошибки при отсутствующем пользователе"""
    response = client.get('/api/general?login=invalid')
    assert response.status_code == 404
    assert 'not found' in response.text.lower()


def test_user_without_actions(client):
    """Проверка пользователя без действий в блоге"""
    response = client.get('/api/general?login=testuser3')
    data = response.json()
    assert data['blog_actions_count'] == 0


def test_user_with_actions(client):
    """Проверка пользователя с действиями в блоге"""
    response = client.get('/api/general?login=testuser2')
    data = response.json()
    assert data['blog_actions_count'] == 3


def test_missing_login_param(client):
    """Проверка отсутствия параметра login"""
    response = client.get('/api/general')
    assert response.status_code == 422
    assert 'field required' in response.text.lower()


def test_user_with_no_logs(client):
    """Проверка пользователя, у которого нет логов"""
    response = client.get('/api/general?login=testuser4')
    assert response.status_code == 200
    data = response.json()
    assert data['blog_actions_count'] == 0
    assert data['login_count'] == 0
    assert data['logout_count'] == 0
    assert 'date' in data


def test_valid_comments_for_testuser2(client):
    """Проверка комментариев для testuser2"""
    response = client.get('/api/comments?login=testuser2')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0] == {
        'login': 'testuser2',
        'post_header': 'Test Post',
        'author_login': 'testuser1',
        'comment_count': 2
    }


def test_multiple_comments_for_testuser3(client):
    """Проверка нескольких комментариев для testuser3"""
    response = client.get('/api/comments?login=testuser3')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    expected_comments = [
        {
            'login': 'testuser3',
            'post_header': 'Test Post 2',
            'author_login': 'testuser2',
            'comment_count': 1,
        },
        {
            'login': 'testuser3',
            'post_header': 'Test Post',
            'author_login': 'testuser1',
            'comment_count': 1,
        },
    ]

    for comment in expected_comments:
        assert comment in data


def test_no_comments(client):
    """Проверка отсутствия комментариев у testuser1"""
    response = client.get('/api/comments?login=testuser1')
    assert response.status_code == 404
    assert 'does not have comments' in response.text.lower()


def test_missing_login_param_comments(client):
    """Проверка отсутствия параметра login"""
    response = client.get('/api/comments')
    assert response.status_code == 422
    assert 'field required' in response.text.lower()
