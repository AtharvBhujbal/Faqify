import json
import pytest
from flask import Flask, jsonify
from unittest.mock import patch, MagicMock


from app.routes import faq_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(faq_bp)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()




@patch("app.routes.db.initialize_database")
@patch("app.routes.logger")
def test_init_db_success(mock_logger, mock_initialize, client):
    """Test /init-db returns a successful JSON response."""
    from app.routes import IS_SUCCESS, STATUS  

    response = client.post("/init-db")
    data = response.get_json()

    
    mock_initialize.assert_called_once()
    
    assert data == IS_SUCCESS["DATABASE_INITIALIZED"]
    assert response.status_code == STATUS["OK"]


@patch("app.routes.db.initialize_database", side_effect=Exception("DB error"))
@patch("app.routes.logger")
def test_init_db_failure(mock_logger, mock_initialize, client):
    """Test /init-db returns an error when initialization fails."""
    from app.routes import IS_ERROR, STATUS

    response = client.post("/init-db")
    data = response.get_json()

    mock_logger.error.assert_called()  
    assert data == IS_ERROR["ERR_DATABASE_INITIALIZATION"]
    assert response.status_code == STATUS["INTERNAL_SERVER_ERROR"]




@patch("app.routes.start_translating_faq_and_caching")
@patch("app.routes.db.create_faq", return_value=123)
def test_create_faq_success(mock_create_faq, mock_translate_and_cache, client):
    """Test that creating a FAQ with valid language works."""
    from app.routes import STATUS

    faq_data = {
        "question": "What is testing?",
        "answer": "Testing is important."
    }
    
    response = client.post("/create-faq?lang=en",
                           data=json.dumps(faq_data),
                           content_type="application/json")
    data = response.get_json()

    
    mock_create_faq.assert_called_once_with(faq_data["question"], faq_data["answer"])
    mock_translate_and_cache.assert_called_once_with(123, "en")

    assert "faq_id" in data
    assert response.status_code == STATUS["OK"]


@patch("app.routes.db.create_faq")
@patch("app.routes.logger")
def test_create_faq_invalid_language(mock_logger, mock_create_faq, client):
    """Test that create-faq returns BAD_REQUEST for an invalid language."""
    from app.routes import IS_ERROR, STATUS

    faq_data = {
        "question": "What is testing?",
        "answer": "Testing is important."
    }
    
    response = client.post("/create-faq?lang=xx",
                           data=json.dumps(faq_data),
                           content_type="application/json")
    data = response.get_json()

    mock_logger.error.assert_called()
    
    mock_create_faq.assert_not_called()
    assert data == IS_ERROR["ERR_FAQ_INVALID_LANG"]
    assert response.status_code == STATUS["BAD_REQUEST"]


@patch("app.routes.db.create_faq", side_effect=Exception("DB error"))
@patch("app.routes.logger")
def test_create_faq_exception(mock_logger, mock_create_faq, client):
    """Test that create-faq returns INTERNAL_SERVER_ERROR on exception."""
    from app.routes import IS_ERROR, STATUS

    faq_data = {
        "question": "What is testing?",
        "answer": "Testing is important."
    }
    response = client.post("/create-faq?lang=en",
                           data=json.dumps(faq_data),
                           content_type="application/json")
    data = response.get_json()

    mock_logger.error.assert_called()
    assert data == IS_ERROR["ERR_FAQ_CREATE"]
    assert response.status_code == STATUS["INTERNAL_SERVER_ERROR"]




@patch("app.routes.db.get_faq", return_value=(1, "What is testing?", "Testing is important?"))
def test_get_faq_found(mock_get_faq, client):
    """Test that getting a FAQ returns the FAQ when found."""
    from app.routes import STATUS

    response = client.get("/faq/1")
    data = response.get_json()

    mock_get_faq.assert_called_once_with(1)
    assert "faq" in data
    assert response.status_code == STATUS["OK"]


@patch("app.routes.db.get_faq", return_value=None)
def test_get_faq_not_found(mock_get_faq, client):
    """Test that getting a non-existent FAQ returns a not found error."""
    from app.routes import IS_ERROR, STATUS

    response = client.get("/faq/999")
    data = response.get_json()

    assert data == IS_ERROR["ERR_FAQ_NOT_FOUND"]
    assert response.status_code == STATUS["NOT_FOUND"]


@patch("app.routes.db.get_faq", side_effect=Exception("DB error"))
@patch("app.routes.logger")
def test_get_faq_exception(mock_logger, mock_get_faq, client):
    """Test that an exception during FAQ fetch returns an error."""
    from app.routes import IS_ERROR, STATUS

    response = client.get("/faq/1")
    data = response.get_json()

    mock_logger.error.assert_called()
    assert data == IS_ERROR["ERR_FAQ_FETCH"]
    assert response.status_code == STATUS["INTERNAL_SERVER_ERROR"]




@patch("app.routes.cache")
@patch("app.routes.translate_all_faqs")
@patch("app.routes.db.get_all_faqs")
def test_faq_route_cached(mock_get_all_faqs, mock_translate_all_faqs, mock_cache, client):
    """Test the faqs route returns cached FAQs if available."""
    from app.routes import STATUS

    
    mock_cache.exists.return_value = True
    cached_faqs = [{"id": 1, "question": "Cached Q?", "answer": "Cached A"}]
    mock_cache.get.return_value = cached_faqs

    response = client.get("/faqs/?lang=es")
    data = response.get_json()

    
    mock_translate_all_faqs.assert_not_called()
    mock_get_all_faqs.assert_not_called()
    mock_cache.exists.assert_called_once_with("es")
    mock_cache.get.assert_called_once_with("es")

    assert data == {"faqs": cached_faqs}
    assert response.status_code == STATUS["OK"]


@patch("app.routes.cache")
@patch("app.routes.translate_all_faqs")
@patch("app.routes.db.get_all_faqs")
def test_faq_route_translate_non_en(mock_get_all_faqs, mock_translate_all_faqs, mock_cache, client):
    """Test the faqs route when language is not 'en' and cache is empty."""
    from app.routes import STATUS

    
    mock_cache.exists.return_value = False
    faqs_from_db = [{"id": 1, "question": "Q?", "answer": "A"}]
    mock_get_all_faqs.return_value = faqs_from_db

    response = client.get("/faqs/?lang=es")
    data = response.get_json()

    
    mock_translate_all_faqs.assert_called_once_with("es")
    mock_get_all_faqs.assert_called_once_with("es")
    mock_cache.set.assert_called_once_with(key="es", value=faqs_from_db)

    assert data == {"faqs": faqs_from_db}
    assert response.status_code == STATUS["OK"]


@patch("app.routes.cache")
@patch("app.routes.db.get_all_faqs")
def test_faq_route_default_en(mock_get_all_faqs, mock_cache, client):
    """Test the faqs route when language is 'en' (default)."""
    from app.routes import STATUS

    mock_cache.exists.return_value = False
    faqs_from_db = [{"id": 1, "question": "Q?", "answer": "A"}]
    mock_get_all_faqs.return_value = faqs_from_db

    response = client.get("/faqs/")  
    data = response.get_json()

    mock_get_all_faqs.assert_called_once_with()
    mock_cache.set.assert_called_once_with(key="en", value=faqs_from_db)
    assert data == {"faqs": faqs_from_db}
    assert response.status_code == STATUS["OK"]


@patch("app.routes.cache")
@patch("app.routes.logger")
def test_faq_route_invalid_language(mock_logger, mock_cache, client):
    """Test the faqs route returns error for invalid language."""
    from app.routes import IS_ERROR, STATUS

    
    response = client.get("/faqs/?lang=xx")
    data = response.get_json()

    mock_logger.error.assert_called()
    assert data == IS_ERROR["ERR_FAQ_INVALID_LANG"]
    assert response.status_code == STATUS["BAD_REQUEST"]


@patch("app.routes.cache")
@patch("app.routes.logger")
def test_faq_route_exception(mock_logger, mock_cache, client):
    """Test that an exception in the faqs route returns an error."""
    from app.routes import IS_ERROR, STATUS

    
    mock_cache.exists.side_effect = Exception("cache error")

    response = client.get("/faqs/?lang=en")
    data = response.get_json()

    mock_logger.error.assert_called()
    assert data == IS_ERROR["ERR_FAQ_FETCH"]
    assert response.status_code == STATUS["INTERNAL_SERVER_ERROR"]


