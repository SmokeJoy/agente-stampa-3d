"""Configurazione dei test con fixture globali."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.utils.mock_redis import mock_redis_client


@pytest.fixture(autouse=True, scope="session")
def redis_patch():
    """Patches default_redis_client per tutti i test della sessione.

    Questa fixture è autouse=True con scope "session", quindi si attiva
    automaticamente una sola volta all'inizio della sessione di test.

    Returns:
        MockRedisClient: Mock Redis client che simula le operazioni in memoria
    """
    # Patchiamo il client Redis sia in services.redis che in utils.ratelimit
    with (
        patch("services.redis.redis_client.default_redis_client", mock_redis_client),
        patch("utils.ratelimit.default_redis_client", mock_redis_client),
    ):
        yield mock_redis_client


@pytest.fixture(scope="function")
def test_client():
    """Fixture per creare un TestClient con Redis già patchato.

    Assicura che l'app venga importata solo DOPO che il patch Redis è attivo.

    Returns:
        TestClient: Client di FastAPI per i test
    """
    # Import main solo dopo che il patch Redis è attivo
    from main import API_PREFIX, app

    # Creiamo un TestClient
    client = TestClient(app)

    # Yield sia il client che l'API_PREFIX
    yield client, API_PREFIX


@pytest.fixture(scope="function")
def rate_limited_client():
    """TestClient con rate_limit reale (non patchato) ma Redis fake.

    Utile per testare effettivamente il funzionamento del rate limit
    senza dover effettuare connessioni a Redis reali.

    Returns:
        TestClient: Client di FastAPI per i test di rate limiting
    """
    # Reset del mock Redis per avere un ambiente pulito
    mock_redis_client.set_current_time(1000.0)

    # Importiamo main solo dopo aver patchato Redis
    from main import API_PREFIX, app

    # Creiamo un TestClient senza patchare il rate_limit
    client = TestClient(app)

    # Yield sia il client che l'API_PREFIX
    yield client, API_PREFIX
