from googletrans import Translator
from .database import db
import asyncio


async def _translate_text(text, dest):
    translator = Translator()
    return await translator.translate(text, dest=dest)


async def _translate_faq(faq_id):
    faq = db.get_faq(faq_id)
    if faq:
        id, question = faq[0],faq[1]
        question_hi = await _translate_text(question, "hi")
        question_bn = await _translate_text(question, "bn") 
        db.update_translation(id, question_hi.text, question_bn.text)


def translate_faq(faq_id):
    asyncio.run(_translate_faq(faq_id))