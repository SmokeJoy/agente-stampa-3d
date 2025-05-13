from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Configure logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_credentials(scopes: list[str]) -> Credentials:
    creds: Credentials | None = None
    token_file = settings.google_token_file

    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_file), scopes)
            logger.info("Credenziali caricate da %s", token_file)
        except Exception as e:
            logger.error("Errore durante il caricamento delle credenziali da %s: %s", token_file, e)
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Token refresh riuscito")
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                logger.info("Token aggiornato salvato in %s", token_file)
            except Exception as e:
                logger.error("Errore durante il refresh del token: %s", e)
                creds = None
        
        if not creds or not creds.valid:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(settings.google_client_secret_file), scopes
                )
                creds = flow.run_local_server(port=settings.google_oauth_port)
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                logger.info("Nuovo token salvato in %s", token_file)
            except FileNotFoundError:
                logger.error("File client_secret.json non trovato in %s. Impossibile procedere con l'autenticazione.", settings.google_client_secret_file)
                return None
            except Exception as e:
                logger.error("Errore durante il flusso di autorizzazione: %s", e)
                return None

    return creds 