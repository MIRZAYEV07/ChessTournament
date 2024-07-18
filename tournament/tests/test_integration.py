import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from tournament.models import Tournament, Match
from user.models import Player


@pytest.mark.django_db
def test_tournament_and_match_integration():
    client = APIClient()
    admin_user = User.objects.create_superuser(
        username="admin", password="password", email="admin@example.com"
    )

    # Force authentication
    client.force_authenticate(user=admin_user)

    # Create tournament
    response = client.post(
        reverse("tournament-list-create"),
        {
            "name": "Integration Tournament",
            "start_date": "2024-07-01",
            "end_date": "2024-07-10",
            "participants": [],
        },
    )
    assert response.status_code == 201
