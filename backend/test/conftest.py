# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    """Client FastAPI pour les tests"""
    return TestClient(app)

@pytest.fixture
def sample_ticket():
    """Fixture avec des données de test"""
    return {
        "title": "Ticket de test",
        "description": "Description de test",
        "priority": "High",
        "status": "Open",
        "tags": [ "test", "test2" ],
        "createdAt": "2026-01-30"
    }