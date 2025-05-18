import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Importa le settings e la funzione da testare
from config.settings import settings
from services.google_calendar.auth_flow import load_credentials

# Definisci uno scope di esempio per i test
TEST_SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]


@pytest.fixture
def mock_settings(tmp_path: Path):
    """Fixture per mockare i percorsi dei file nelle settings."""
    original_token_file = settings.google_token_file
    original_secret_file = settings.google_client_secret_file

    mock_token_path = tmp_path / "mock_token.json"
    mock_secret_path = tmp_path / "mock_client_secret.json"

    settings.google_token_file = mock_token_path
    settings.google_client_secret_file = mock_secret_path

    yield mock_token_path, mock_secret_path

    settings.google_token_file = original_token_file
    settings.google_client_secret_file = original_secret_file


@patch("services.google_calendar.auth_flow.Credentials")
@patch("services.google_calendar.auth_flow.InstalledAppFlow")
def test_load_credentials_new_token_flow(
    MockInstalledAppFlow: MagicMock,
    MockCredentials: MagicMock,
    mock_settings: tuple[Path, Path],
):
    """Testa il flusso di creazione di un nuovo token quando token.json non esiste."""
    mock_token_file, mock_client_secret_file = mock_settings

    if mock_token_file.exists():
        mock_token_file.unlink()

    mock_client_secret_data = {
        "installed": {
            "client_id": "test_client_id",
            "project_id": "test_project_id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "test_client_secret",  # pragma: allowlist secret
            "redirect_uris": ["http://localhost"],
        }
    }
    mock_client_secret_file.write_text(json.dumps(mock_client_secret_data))

    mock_flow_instance = MockInstalledAppFlow.from_client_secrets_file.return_value
    mock_creds_object = MockCredentials.return_value
    mock_creds_object.to_json.return_value = '{"token": "mock_token_value"}'
    mock_creds_object.valid = True
    mock_flow_instance.run_local_server.return_value = mock_creds_object

    credentials = load_credentials(scopes=TEST_SCOPES)

    MockInstalledAppFlow.from_client_secrets_file.assert_called_once_with(str(mock_client_secret_file), TEST_SCOPES)
    mock_flow_instance.run_local_server.assert_called_once_with(port=settings.google_oauth_port)
    assert mock_token_file.exists(), "Il file token.json mockato dovrebbe essere stato creato"
    assert mock_token_file.read_text() == '{"token": "mock_token_value"}'
    assert credentials == mock_creds_object
    assert credentials.valid


@patch("services.google_calendar.auth_flow.Credentials")
@patch("services.google_calendar.auth_flow.InstalledAppFlow")
def test_load_credentials_existing_valid_token(
    MockInstalledAppFlow: MagicMock,
    MockCredentials: MagicMock,
    mock_settings: tuple[Path, Path],
):
    """Testa il caricamento di credenziali valide da un token.json esistente."""
    mock_token_file, _ = mock_settings

    mock_valid_token_data = {
        "token": "valid_mock_token",
        "refresh_token": "mock_refresh",
        "scopes": ["test_scope"],
        "client_id": "id",
        "client_secret": "secret",  # pragma: allowlist secret
    }
    mock_token_file.write_text(json.dumps(mock_valid_token_data))

    mock_creds_instance = MockCredentials.from_authorized_user_file.return_value
    mock_creds_instance.valid = True

    credentials = load_credentials(scopes=TEST_SCOPES)

    MockCredentials.from_authorized_user_file.assert_called_once_with(str(mock_token_file), TEST_SCOPES)
    MockInstalledAppFlow.from_client_secrets_file.assert_not_called()
    assert credentials == mock_creds_instance
    assert credentials.valid


@patch("services.google_calendar.auth_flow.Request")
@patch("services.google_calendar.auth_flow.Credentials")
@patch("services.google_calendar.auth_flow.InstalledAppFlow")
def test_load_credentials_expired_token_refresh_success(
    MockInstalledAppFlow: MagicMock,
    MockCredentials: MagicMock,
    MockRequest: MagicMock,
    mock_settings: tuple[Path, Path],
):
    """Testa il refresh di un token scaduto che va a buon fine."""
    mock_token_file, _ = mock_settings

    mock_expired_token_data = {
        "token": "expired_token",
        "refresh_token": "valid_refresh_token",
        "scopes": ["test_scope"],
        "client_id": "id",
        "client_secret": "secret",  # pragma: allowlist secret
        "expiry": "2000-01-01T00:00:00Z",
    }
    mock_token_file.write_text(json.dumps(mock_expired_token_data))

    mock_creds_instance = MockCredentials.from_authorized_user_file.return_value
    mock_creds_instance.valid = False
    mock_creds_instance.expired = True
    mock_creds_instance.refresh_token = "valid_refresh_token"

    def refresh_side_effect(request):
        mock_creds_instance.valid = True
        mock_creds_instance.expired = False
        mock_creds_instance.token = "refreshed_token"
        mock_creds_instance.to_json.return_value = (
            '{"token": "refreshed_token", "refresh_token": "valid_refresh_token"}'
        )
        return None

    mock_creds_instance.refresh.side_effect = refresh_side_effect

    credentials = load_credentials(scopes=TEST_SCOPES)

    MockCredentials.from_authorized_user_file.assert_called_once_with(str(mock_token_file), TEST_SCOPES)
    mock_creds_instance.refresh.assert_called_once_with(MockRequest())
    MockInstalledAppFlow.from_client_secrets_file.assert_not_called()
    assert mock_token_file.read_text() == ('{"token": "refreshed_token", "refresh_token": "valid_refresh_token"}')
    assert credentials == mock_creds_instance
    assert credentials.valid


# TODO: Aggiungere test per i casi di fallimento del refresh e
#       quando client_secret.json non viene trovato (dovrebbe restituire None
#       e loggare errore).
