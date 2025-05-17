"""Redis mock per i test."""

import time
from typing import Dict, Optional, Set, Tuple, Union

from services.redis.redis_client import RedisClient


class MockRedisClient(RedisClient):
    """Mock di RedisClient per i test che simula il comportamento di Redis in memoria."""

    def __init__(self):
        """Inizializza il mock client."""
        super().__init__()
        self._data: Dict[str, Union[str, int, float, Set[Tuple[str, float]]]] = {}
        self._ttls: Dict[str, float] = {}
        self._current_time = 1000.0  # Timestamp iniziale arbitrario

    @property
    def client(self):
        """Ritorna self poiché questo mock implementa direttamente i metodi Redis."""
        return self

    def time(self) -> Tuple[int, int]:
        """Simula il comando Redis TIME.

        Returns:
            Tuple[int, int]: Timestamp in formato (seconds, microseconds)
        """
        seconds = int(self._current_time)
        microseconds = int((self._current_time - seconds) * 1000000)
        return [seconds, microseconds]

    def incr(self, key: str, amount: int = 1) -> int:
        """Incrementa un contatore.

        Args:
            key: Chiave del contatore
            amount: Quantità da incrementare

        Returns:
            int: Nuovo valore
        """
        if key not in self._data:
            self._data[key] = 0
        self._data[key] = int(self._data[key]) + amount
        return self._data[key]

    def zadd(self, key: str, mapping: Dict[str, float]) -> int:
        """Aggiunge membri a un sorted set.

        Args:
            key: Chiave del sorted set
            mapping: Mapping tra membri e score

        Returns:
            int: Numero di elementi aggiunti
        """
        if key not in self._data:
            self._data[key] = set()

        added = 0
        for member, score in mapping.items():
            # In Redis non è possibile avere duplicati nei set
            # Quindi aggiungiamo solo se il membro non esiste
            exists = False
            for existing_member, _ in self._data[key]:
                if existing_member == member:
                    exists = True
                    break

            if not exists:
                self._data[key].add((member, score))
                added += 1

        return added

    def zcard(self, key: str) -> int:
        """Conta il numero di membri in un sorted set.

        Args:
            key: Chiave del sorted set

        Returns:
            int: Numero di membri
        """
        if key not in self._data:
            return 0
        return len(self._data[key])

    def zremrangebyscore(self, key: str, min_score: float, max_score: float) -> int:
        """Rimuove membri da un sorted set in base allo score.

        Args:
            key: Chiave del sorted set
            min_score: Score minimo (incluso)
            max_score: Score massimo (incluso)

        Returns:
            int: Numero di membri rimossi
        """
        if key not in self._data:
            return 0

        # Crea una lista per i membri da conservare
        members_to_keep = set()
        removed = 0

        # Per ogni membro nel set
        for member, score in self._data[key]:
            # Se lo score è fuori dal range, mantieni il membro
            if score < min_score or score > max_score:
                members_to_keep.add((member, score))
            else:
                removed += 1

        # Aggiorna il set con i membri da mantenere
        self._data[key] = members_to_keep
        return removed

    def exists(self, key: str) -> bool:
        """Verifica se una chiave esiste.

        Args:
            key: Chiave da verificare

        Returns:
            bool: True se la chiave esiste, False altrimenti
        """
        return key in self._data

    def expire(self, key: str, seconds: int) -> bool:
        """Imposta un TTL su una chiave.

        Args:
            key: Chiave su cui impostare il TTL
            seconds: Numero di secondi prima della scadenza

        Returns:
            bool: True se il TTL è stato impostato, False altrimenti
        """
        if key not in self._data:
            return False

        # Imposta il timestamp di scadenza
        self._ttls[key] = self._current_time + seconds
        return True

    def ttl(self, key: str) -> int:
        """Ritorna il TTL di una chiave.

        Args:
            key: Chiave di cui ottenere il TTL

        Returns:
            int: TTL in secondi, -1 se la chiave non ha TTL, -2 se la chiave non esiste
        """
        if key not in self._data:
            return -2

        if key not in self._ttls:
            return -1

        # Calcola il TTL rimanente
        remaining = self._ttls[key] - self._current_time
        if remaining <= 0:
            # La chiave è scaduta, la rimuoviamo
            del self._data[key]
            del self._ttls[key]
            return -2

        return int(remaining)

    def get(self, key: str) -> Optional[str]:
        """Ottiene il valore di una chiave.

        Args:
            key: Chiave da cui ottenere il valore

        Returns:
            str: Valore della chiave, None se la chiave non esiste
        """
        if key not in self._data:
            return None
        return str(self._data[key])

    def set(
        self, key: str, value: Union[str, bytes, int, float], ex: Optional[int] = None
    ) -> bool:
        """Imposta il valore di una chiave.

        Args:
            key: Chiave da impostare
            value: Valore da impostare
            ex: TTL in secondi (opzionale)

        Returns:
            bool: True se l'operazione è riuscita
        """
        self._data[key] = value

        if ex is not None:
            self.expire(key, ex)

        return True

    def delete(self, key: str) -> bool:
        """Elimina una chiave.

        Args:
            key: Chiave da eliminare

        Returns:
            bool: True se la chiave è stata eliminata, False se la chiave non esisteva
        """
        if key not in self._data:
            return False

        del self._data[key]
        if key in self._ttls:
            del self._ttls[key]

        return True

    def set_current_time(self, seconds: float) -> None:
        """Imposta il timestamp corrente per i test.

        Args:
            seconds: Timestamp in secondi
        """
        self._current_time = seconds


# Mock singleton che verrà usato nei test
mock_redis_client = MockRedisClient()
