"""Router per gli endpoint relativi ai lavori di stampa 3D."""

from typing import List, Optional

from fastapi import APIRouter, Query, status

from services.jobs_service import search_jobs

# Crea router con tags
router = APIRouter(
    tags=["jobs"],
)


@router.get(
    "/searchJobs",
    summary="Cerca lavori di stampa 3D",
    description=(
        "Cerca lavori di stampa 3D disponibili in base a parola chiave, posizione, "
        "budget e tag. Restituisce una lista di lavori corrispondenti."
    ),
    response_description="Risultati della ricerca di lavori di stampa 3D",
    status_code=status.HTTP_200_OK,
)
async def search_jobs_endpoint(
    keyword: Optional[str] = Query(
        None,
        description="Parola chiave per la ricerca dei lavori",
    ),
    location: Optional[str] = Query(
        None,
        description="Posizione geografica dei lavori",
    ),
    min_budget: Optional[float] = Query(
        None,
        description="Budget minimo per i lavori (exclusiveMinimum: 0)",
        gt=0,
    ),
    max_budget: Optional[float] = Query(
        None,
        description="Budget massimo per i lavori",
        gt=0,
    ),
    tags: Optional[List[str]] = Query(
        None,
        description="Lista di tag per filtrare i lavori",
    ),
    page: int = Query(
        1,
        description="Numero di pagina per la paginazione",
        ge=1,
    ),
    page_size: int = Query(
        10,
        description="Numero di risultati per pagina",
        ge=1,
        le=100,
    ),
):
    """Cerca lavori di stampa 3D in base ai parametri forniti.

    Args:
        keyword: Parola chiave per la ricerca
        location: Filtro per posizione
        min_budget: Budget minimo (deve essere > 0)
        max_budget: Budget massimo (deve essere > 0)
        tags: Lista di tag per filtrare i lavori
        page: Numero di pagina per la paginazione
        page_size: Numero di risultati per pagina

    Returns:
        dict: Risultati della ricerca, contiene jobs e metadati di paginazione
    """
    # Effettua la ricerca attraverso il servizio
    result = await search_jobs(
        keyword=keyword,
        location=location,
        min_budget=min_budget,
        max_budget=max_budget,
        tags=tags,
        page=page,
        page_size=page_size,
    )

    # Restituisci il risultato
    return result.model_dump()
