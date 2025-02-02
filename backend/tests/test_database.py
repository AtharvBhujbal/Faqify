import pytest
from app.database import database

@pytest.fixture(scope="module")
def db_instance():
    db = database()
    db.initialize_database()
    yield db


def test_create_faq(db_instance):
    faq_id = db_instance.create_faq("What is Python?", "Python is a high-level programming language.")
    assert isinstance(faq_id, int)


def test_get_faq(db_instance):
    faq_id = db_instance.create_faq("What is a database?", "A database is an organized collection of data.")
    faq = db_instance.get_faq(faq_id)
    assert faq is not None
    assert faq[1] == "What is a database?"
    assert faq[4] == "A database is an organized collection of data."


def test_get_all_faqs(db_instance):
    db_instance.create_faq("What is machine learning?", "Machine learning is a subset of artificial intelligence.")
    faqs = db_instance.get_all_faqs()
    assert len(faqs) >= 1


def test_get_all_not_translated_faqs(db_instance):
    faqs = db_instance.get_all_not_translated_faqs()
    assert isinstance(faqs, list)


def test_update_faq(db_instance):
    faq_id = db_instance.create_faq("What is SQL?", "SQL stands for Structured Query Language.")
    db_instance.update_faq(faq_id, "What is SQL?", "SQL is used to manage and manipulate databases.")
    faq = db_instance.get_faq(faq_id)
    assert faq[4] == "SQL is used to manage and manipulate databases."


def test_update_translation(db_instance):
    faq_id = db_instance.create_faq("What is an API?", "API stands for Application Programming Interface.")
    db_instance.update_translation(faq_id, "¿Qué es una API?", "es")
    faq = db_instance.get_faq(faq_id)
    assert faq[2] == "¿Qué es una API?"
    assert faq[3] == "es"
