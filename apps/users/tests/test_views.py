import pytest


@pytest.mark.django_db
def test_register(api_client):
    data = {
        "email": "test@test.com",
        "password": "testpass123",
        "password2": "testpass123",
    }

    response = api_client.post("/api/v1/users/register/", data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_login(api_client, user):
    data = {
        "email": "example@example.com",
        "password": "testpass123",
    }

    response = api_client.post("/api/v1/users/login/", data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_registration_fails_when_passwords_do_not_match(api_client):
    data = {
        "email": "test@test.com",
        "password": "testpass123",
        "password2": "testpass321",
    }

    response = api_client.post("/api/v1/users/register/", data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_email_exists(api_client, user):
    data = {
        "email": "example@example.com",
        "password": "testpass123",
        "password2": "testpass123",
    }

    response = api_client.post("/api/v1/users/register/", data)
    assert "email" in response.data
    assert response.data["email"][0] == "Данный email уже зарегистрирован"
    assert response.status_code == 400


@pytest.mark.django_db
def test_incorrect_password(api_client, user):
    data = {
        "email": "example@example.com",
        "password": "testpass321",
    }

    response = api_client.post("/api/v1/users/login/", data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_me(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/v1/users/me/")
    assert response.status_code == 200
    assert response.data["email"] == user.email
