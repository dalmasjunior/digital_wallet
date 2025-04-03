import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    response = client.post("/api/auth/register/", {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testuser").exists()

@pytest.mark.django_db
def test_login_user():
    client = APIClient()
    User.objects.create_user(username="testuser", password="testpassword")
    
    response = client.post("/api/auth/login/", {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
