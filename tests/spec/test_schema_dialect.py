"""Test per validare il dialect JSON Schema e lo schema OpenAPI 3.1."""

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate


@pytest.fixture
def root_dir():
    """Restituisce il percorso della root del progetto."""
    # Il test è in tests/spec, quindi dobbiamo risalire di due livelli
    return Path(__file__).parent.parent.parent


@pytest.fixture
def mif_dialect_schema(root_dir):
    """Carica il MIF JSON Schema Dialect."""
    dialect_path = root_dir / "mif_jsonschema_dialect.json"
    assert dialect_path.exists(), f"Dialect schema file non trovato: {dialect_path}"

    with open(dialect_path, "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def openapi_schema(root_dir):
    """Carica lo schema OpenAPI 3.1."""
    openapi_path = root_dir / "openapi_3_1_demo.json"
    assert openapi_path.exists(), f"OpenAPI schema file non trovato: {openapi_path}"

    with open(openapi_path, "r", encoding="utf-8") as file:
        return json.load(file)


def test_dialect_schema_is_valid(mif_dialect_schema):
    """Verifica che il dialect schema sia un JSON Schema valido."""
    # Verifica che il dialect abbia i campi obbligatori
    assert "$schema" in mif_dialect_schema, "Dialect schema manca del campo $schema"
    assert "$id" in mif_dialect_schema, "Dialect schema manca del campo $id"
    assert "title" in mif_dialect_schema, "Dialect schema manca del campo title"
    assert "properties" in mif_dialect_schema, "Dialect schema manca del campo properties"

    # Verifica che il dialect specifichi l'endpoint $schema corretto
    assert (
        mif_dialect_schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    ), "Dialect schema deve riferirsi a draft 2020-12 di JSON Schema"

    # Verifica che il dialect abbia un $id valido e univoco
    assert mif_dialect_schema["$id"].startswith("https://"), "Dialect schema deve avere un $id che inizia con https://"


def test_dialect_contains_custom_keywords(mif_dialect_schema):
    """Verifica che il dialect contenga le keyword custom richieste."""
    # Verifica x-internal
    path_props = mif_dialect_schema["properties"]["paths"]["patternProperties"]["^/"]["properties"]
    assert "x-internal" in path_props, "Dialect manca della keyword x-internal per paths"

    # Verifica x-risk
    schema_props = mif_dialect_schema["properties"]["components"]["properties"]["schemas"]["patternProperties"][
        "^[a-zA-Z0-9._-]+$"
    ]["properties"]
    assert "x-risk" in schema_props, "Dialect manca della keyword x-risk per schemas"

    # Verifica enum values per x-risk
    risk_levels = schema_props["x-risk"]["enum"]
    expected_levels = ["low", "medium", "high", "critical"]
    assert all(
        level in risk_levels for level in expected_levels
    ), f"x-risk deve supportare tutti i livelli di rischio: {expected_levels}"


def test_openapi_schema_validates_against_dialect(openapi_schema, mif_dialect_schema):
    """Verifica che lo schema OpenAPI 3.1 sia valido secondo il dialect."""
    try:
        validate(instance=openapi_schema, schema=mif_dialect_schema)
    except ValidationError as e:
        pytest.fail(f"OpenAPI schema non è valido secondo il dialect: {e}")


def test_openapi_contains_required_fields(openapi_schema):
    """Verifica che lo schema OpenAPI contenga tutti i campi obbligatori."""
    assert "openapi" in openapi_schema, "OpenAPI schema manca del campo openapi"
    assert openapi_schema["openapi"] == "3.1.0", "OpenAPI versione deve essere 3.1.0"

    assert "info" in openapi_schema, "OpenAPI schema manca della sezione info"
    assert "title" in openapi_schema["info"], "OpenAPI info manca del campo title"
    assert "version" in openapi_schema["info"], "OpenAPI info manca del campo version"

    assert "paths" in openapi_schema, "OpenAPI schema manca della sezione paths"
