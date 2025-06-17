from fastapi import status
from .utils import client


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
