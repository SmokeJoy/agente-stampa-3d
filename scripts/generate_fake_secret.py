import json
from pathlib import Path

# Definisci il percorso in cui salvare il file client_secret.json fittizio
# Questo dovrebbe corrispondere al percorso atteso dai test o dalla
# configurazione di default quando le vere credenziali non sono
# disponibili (es. in CI).
DEFAULT_SECRETS_DIR = Path(__file__).parent.parent / "secrets"
FAKE_SECRET_FILE_PATH = DEFAULT_SECRETS_DIR / "client_secret.json"


def generate_fake_google_secret_file(
    output_path: Path = FAKE_SECRET_FILE_PATH,
) -> None:
    """
    Genera un file client_secret.json fittizio per Google OAuth.

    Questo file contiene la struttura minima richiesta affinché le librerie
    client possano caricarlo senza errori durante i test in ambienti CI,
    dove le vere credenziali non dovrebbero essere presenti.
    """
    fake_secret_content = {
        "installed": {
            "client_id": "fake_client_id.apps.googleusercontent.com",
            "project_id": "fake-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": (
                "https://www.googleapis.com/oauth2/v1/certs"
            ),
            "client_secret": "FAKE_CLIENT_SECRET_VALUE",  # pragma: allowlist secret
            "redirect_uris": [
                # Corrisponde a settings.google_oauth_port (default)
                "http://localhost:8765/",
                "urn:ietf:wg:oauth:2.0:oob",
            ],
        }
    }

    # Assicurati che la directory esista
    output_path.parent.mkdir(parents=True, exist_ok=True)  # noqa: E501

    with open(output_path, "w") as f:
        json.dump(fake_secret_content, f, indent=4)

    print(f"File client_secret.json fittizio generato in: {output_path}")


if __name__ == "__main__":
    print(
        "Generazione del file client_secret.json fittizio " "per ambienti di test/CI..."
    )
    generate_fake_google_secret_file()
    print("Script completato.")
    print(
        "Ricorda di assicurarti che la directory 'secrets/' sia nel tuo .gitignore"  # noqa: E501
    )
    print(
        "e che questo file fittizio sia disponibile nel percorso corretto "  # noqa: E501
        "durante i test in CI."
    )
