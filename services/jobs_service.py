"""Servizio per la ricerca di lavori di stampa 3D.

Questo modulo implementa la logica di business per il servizio di ricerca dei lavori,
permettendo di filtrare in base a parole chiave, posizione, budget e tag.  # noqa: E501
"""

from typing import List, Optional
from uuid import UUID

from pydantic.fields import Field
from pydantic.main import BaseModel


class Job(BaseModel):
    """Modello dati per un lavoro di stampa 3D."""

    id: UUID
    title: str
    description: Optional[str] = None
    # Budget deve essere maggiore di 10 (exclusiveMinimum)
    budget: float = Field(..., gt=10)
    # Payout deve essere minore di 1000 (exclusiveMaximum)
    max_payout: Optional[float] = Field(None, lt=1000)
    location: Optional[str] = None
    tags: Optional[List[str]] = None


class SearchJobsResult(BaseModel):
    """Risultato di una ricerca di lavori."""

    jobs: List[Job]
    total: int
    page: int
    page_size: int


async def search_jobs(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None,
    tags: Optional[List[str]] = None,
    page: int = 1,
    page_size: int = 10,
) -> SearchJobsResult:
    """Cerca lavori di stampa 3D in base a vari criteri.

    Args:
        keyword: Parola chiave da cercare nel titolo e nella descrizione
        location: Posizione geografica dei lavori
        min_budget: Budget minimo per i lavori
        max_budget: Budget massimo per i lavori
        tags: Lista di tag da filtrare
        page: Numero di pagina per la paginazione
        page_size: Numero di risultati per pagina

    Returns:
        SearchJobsResult: Risultato della ricerca
    """
    # Questa è un'implementazione di esempio - in un'applicazione reale,
    # connetterebbe a un database per recuperare i dati

    # Simuliamo alcuni dati di esempio
    from uuid import uuid4

    # Genera 20 lavori di esempio
    sample_jobs = [
        Job(
            id=uuid4(),
            title=f"Stampa 3D di prototipo {i}",
            description=f"Stampa di un prototipo di prodotto. Dettagli: {keyword if keyword else 'vari'}",  # noqa: E501
            budget=50.0 + i * 10,
            max_payout=500.0 + i * 20,
            location=location if location else "Roma",
            tags=tags if tags else ["prototipo", "industriale"],
        )
        for i in range(1, 21)
    ]

    # Filtra in base ai criteri
    filtered_jobs = sample_jobs.copy()

    if keyword:
        filtered_jobs = [
            job
            for job in filtered_jobs
            if keyword.lower() in job.title.lower() or (job.description and keyword.lower() in job.description.lower())
        ]

    if location:
        filtered_jobs = [
            job for job in filtered_jobs if job.location and location.lower() in job.location.lower()  # noqa: E501
        ]

    if min_budget is not None:
        filtered_jobs = [job for job in filtered_jobs if job.budget >= min_budget]

    if max_budget is not None:
        filtered_jobs = [job for job in filtered_jobs if job.budget <= max_budget]  # noqa: E501

    if tags:
        filtered_jobs = [job for job in filtered_jobs if job.tags and any(tag in job.tags for tag in tags)]

    # Calcola l'offset per la paginazione
    total = len(filtered_jobs)
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total)

    # Ritorna i risultati paginati
    return SearchJobsResult(
        jobs=filtered_jobs[start_idx:end_idx],
        total=total,
        page=page,
        page_size=page_size,
    )
