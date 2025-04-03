import pytest
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from wallets.models import Wallet

@pytest.mark.django_db
def test_create_wallet():
    user = User.objects.create_user(username="testuser", password="testpassword")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/wallets/", {"name": "Main Wallet"})
    assert response.status_code == status.HTTP_201_CREATED
    assert Wallet.objects.filter(owner=user).exists()

@pytest.mark.django_db
def test_deposit():
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet = Wallet.objects.create(owner=user, balance=0)
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(f"/api/wallets/{wallet.id}/deposit/", {"amount": 100})
    wallet.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert wallet.balance == 100
