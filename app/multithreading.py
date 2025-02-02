
import threading
from dotenv import load_dotenv
load_dotenv()
import os

from .translate import translate_faq, translate_all_faqs
from .message import IND_LANGUAGES
from .redis import cache
from .database import db


def start_translating_faq_and_caching(faq_id, lang):
    t1 = threading.Thread(target=translate_faq, args=(faq_id, lang))
    t1.start()
    t1.join()

    t2 = threading.Thread(target=cache_all_faqs)
    t2.start()
    

def cache_all_faqs():
    if not cache.exists("preprocessed_faqs"):
        cache.flush()
        key = "preprocessed_faqs"
        value = True
        cache.set(key, value, os.getenv('PREPROCESS_EXPIRY_TIME'))
        for lang in IND_LANGUAGES.values():
            translate_all_faqs(lang)
            cache.set(key=lang,value=db.get_all_faqs(lang),expiry=os.getenv('PREPROCESS_EXPIRY_TIME'))
    else:
        pass