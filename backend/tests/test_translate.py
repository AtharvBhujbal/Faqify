from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from app.translate import translate_faq, translate_all_faqs

# If translate_faq is async, you need to mark the test as async too:
@pytest.mark.asyncio
@patch('app.translate.db')
@patch('app.translate.Translator')
async def test_translate_faq(mock_translator, mock_db):
    mock_faq = (1, 'What is Python?')
    mock_db.get_faq.return_value = mock_faq

    # Create an async mock for the translate method
    mock_translation = MagicMock()
    mock_translation.text = '¿Qué es Python?'
    mock_translator.return_value.translate = AsyncMock(return_value=mock_translation)

    # Await the async function
    await translate_faq(1, 'es')

    mock_db.update_translation.assert_called_with(1, '¿Qué es Python?', language='es')


@pytest.mark.asyncio
@patch('app.translate.db')
@patch('app.translate.Translator')
async def test_translate_all_faqs(mock_translator, mock_db):
    mock_faqs = [(1, 'What is Python?'), (2, 'How does Redis work?')]
    mock_db.get_all_faqs.return_value = mock_faqs

    translations = ['¿Qué es Python?', '¿Cómo funciona Redis?']

    # Set up async mocks for each translate call
    mock_translator_instance = mock_translator.return_value
    mock_translator_instance.translate = AsyncMock(side_effect=[
        MagicMock(text=translations[0]),
        MagicMock(text=translations[1])
    ])

    await translate_all_faqs('es')

    mock_db.update_translation.assert_any_call(1, '¿Qué es Python?', language='es')
    mock_db.update_translation.assert_any_call(2, '¿Cómo funciona Redis?', language='es')