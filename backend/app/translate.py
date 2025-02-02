from googletrans import Translator
from .database import db
import asyncio


async def _translate_text(text, dest):
    translator = Translator()
    return await translator.translate(text, dest=dest)


async def _translate_faq(faq_id,lang):
    faq = db.get_faq(faq_id)
    if faq:
        id, question = faq[0],faq[1]
        question_trans = await _translate_text(question, lang)
        db.update_translation(id, question_trans.text,language=lang)

def translate_faq(faq_id,lang):
    asyncio.run(_translate_faq(faq_id,lang))


async def _translate_all_faqs(lang):
    faqs = db.get_all_faqs()
    for faq in faqs:
        id, question = faq[0],faq[1]
        question_trans = await _translate_text(question, lang)
        db.update_translation(id, question_trans.text,language=lang)

def translate_all_faqs(lang):
    asyncio.run(_translate_all_faqs(lang))