"""Tests for the uploader service and validator."""

import pytest

# TODO: Implement actual tests once service logic is in place.


@pytest.mark.skip(reason="TODO: Implement test_valid_stl_upload")
def test_valid_stl_upload():
    """Test uploading a valid STL file."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_valid_obj_upload")
def test_valid_obj_upload():
    """Test uploading a valid OBJ file."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_invalid_mime_type_upload")
def test_invalid_mime_type_upload():
    """Test uploading a file with an invalid MIME type."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_upload_storage_called")
def test_upload_storage_called():
    """Test that the storage backend's save method is called."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_file_id_returned_on_success")
def test_file_id_returned_on_success():
    """Test that a file_id and 'stored' status are returned on successful upload."""
    pass


# Tests for validator.py
@pytest.mark.skip(reason="TODO: Implement test_validator_valid_stl_mime")
def test_validator_valid_stl_mime():
    """Test validator with a valid STL MIME type."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_validator_valid_obj_mime")
def test_validator_valid_obj_mime():
    """Test validator with a valid OBJ MIME type."""
    pass


@pytest.mark.skip(reason="TODO: Implement test_validator_invalid_mime")
def test_validator_invalid_mime():
    """Test validator with an invalid MIME type."""
    pass
