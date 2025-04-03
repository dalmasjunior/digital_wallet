import pytest
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from wallets.models import Wallet

@pytest.mark.django_db
def test_transfer():
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet1 = Wallet.objects.create(owner=user, balance=200)
    wallet2 = Wallet.objects.create(owner=user, balance=50)
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(f"/api/wallets/{wallet1.id}/transfer/", {
        "target_wallet_id": wallet2.id,
        "amount": 100
    })

    wallet1.refresh_from_db()
    wallet2.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert wallet1.balance == 100
    assert wallet2.balance == 150
