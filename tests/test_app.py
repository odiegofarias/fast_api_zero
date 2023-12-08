from fastapi.testclient import TestClient

from fast_zero.app import app
from fast_zero.schemas import UserPublic

client = TestClient(app)


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá, Mundo'}


def test_create_user(client):
    response = client.post(
        '/create_user/',
        json={
            'username': 'Alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'username': 'Alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_usuario_ja_existente(client, user):
    response = client.post(
        '/create_user/',
        json={
            'username': 'test',
            'email': 'test@example.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Email already registered'}


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_editar_usuario_inexistente(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'User not found.'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted.'}


def test_deletar_usuario_inexistente(client, user):
    response = client.delete('/users/2')

    assert response.status_code == 400
    assert response.json() == {'detail': 'User not found.'}
