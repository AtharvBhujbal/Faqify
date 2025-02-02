import os
import threading
from unittest.mock import patch, MagicMock, call
import pytest

from app.multithreading import (
    start_translating_faq_and_caching,
    process_faq_and_cache,
    cache_all_faqs,
)

def test_start_translating_faq_and_caching():
    faq_id = 1
    lang = "es"

    with patch("app.multithreading.threading.Thread") as mock_thread_cls:
        
        fake_thread = MagicMock()
        mock_thread_cls.return_value = fake_thread
        
        start_translating_faq_and_caching(faq_id, lang)
        
        mock_thread_cls.assert_called_once_with(
            target=process_faq_and_cache, args=(faq_id, lang)
        )
        
        fake_thread.start.assert_called_once()


def test_process_faq_and_cache():
    faq_id = 1
    lang = "es"

    with patch("app.multithreading.translate_faq") as mock_translate_faq, \
         patch("app.multithreading.cache_all_faqs") as mock_cache_all:
        process_faq_and_cache(faq_id, lang)

        mock_translate_faq.assert_called_once_with(faq_id, lang)
        
        mock_cache_all.assert_called_once()


def test_cache_all_faqs_when_not_exists():
    dummy_languages = {"es": "es", "fr": "fr"}
    expiry_value = "3600"  

    with patch("app.multithreading.cache") as mock_cache, \
         patch("app.multithreading.translate_all_faqs") as mock_translate_all, \
         patch("app.multithreading.db") as mock_db, \
         patch("app.multithreading.IND_LANGUAGES", new=dummy_languages), \
         patch("os.getenv", return_value=expiry_value) as mock_getenv:
        
        mock_cache.exists.return_value = False

        dummy_faqs = [{"id": 1, "question": "Dummy", "answer": "Dummy answer"}]
        mock_db.get_all_faqs.return_value = dummy_faqs

        cache_all_faqs()

        
        mock_cache.flush.assert_called_once()
        
        mock_cache.set.assert_any_call("preprocessed_faqs", True, expiry_value)
        
        expected_calls = [call("es"), call("fr")]
        assert mock_translate_all.call_args_list == expected_calls

        
        mock_cache.set.assert_any_call(
            key="es", value=mock_db.get_all_faqs("es"), expiry=expiry_value
        )
        mock_cache.set.assert_any_call(
            key="fr", value=mock_db.get_all_faqs("fr"), expiry=expiry_value
        )
        
        
        assert mock_cache.set.call_count == 1 + len(dummy_languages)


def test_cache_all_faqs_when_exists():
    with patch("app.multithreading.cache") as mock_cache, \
         patch("app.multithreading.translate_all_faqs") as mock_translate_all, \
         patch("app.multithreading.db") as mock_db:
        
        mock_cache.exists.return_value = True

        cache_all_faqs()
        
        mock_cache.flush.assert_not_called()
        
        mock_translate_all.assert_not_called()
        mock_cache.set.assert_not_called()
