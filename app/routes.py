from flask import Blueprint, render_template, jsonify, request
faq_bp = Blueprint('faq', __name__)
import requests
import threading
from googletrans import LANGUAGES

from .database import db
from .message import IS_SUCCESS, IS_ERROR, STATUS
from .log import logger
from .translate import translate_faq, translate_all_faqs

@faq_bp.route('/')
def hello():
    return render_template('index.html')


@faq_bp.route('/init-db',methods=['POST'])
def init_db():
    try:
        db.initialize_database()
        resp = IS_SUCCESS["DATABASE_INITIALIZED"]
        status = STATUS["OK"]

    except Exception as e:
        logger.error(f"Database Error: {e}")
        resp = IS_ERROR["ERR_DATABASE_INITIALIZATION"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status


@faq_bp.route('/create-faq',methods=['POST'])
def create_faq():
    try:
        lang = request.args.get("lang", "en")
        if lang and lang not in LANGUAGES:
            raise ValueError("Invalid Language")
        
        data = request.get_json()
        faq_id = db.create_faq(data["question"], data["answer"])

        thread = threading.Thread(target=translate_faq, args=(faq_id,lang))
        thread.start()

        resp = {"faq_id": faq_id}
        status = STATUS["OK"]

    except ValueError as e:
        resp = IS_ERROR["ERR_FAQ_INVALID_LANG"]
        status = STATUS["BAD_REQUEST"]
        logger.error(f"Invalid Language: {e}")
    
    except Exception as e:
        resp = IS_ERROR["ERR_FAQ_CREATE"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
        logger.error(f"Database Error: {e}")
    
    return jsonify(resp), status


@faq_bp.route('/faq/<int:faq_id>',methods=['GET'])
def get_faq(faq_id):
    try:
        faq = db.get_faq(faq_id)
        if faq:
            resp = {"faq": faq}
            status = STATUS["OK"]
        else:
            resp = IS_ERROR["ERR_FAQ_NOT_FOUND"]
            status = STATUS["NOT_FOUND"]
    
    except Exception as e:
        resp = IS_ERROR["ERR_FAQ_FETCH"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
        logger.error(f"Database Error: {e}")
    
    return jsonify(resp), status


@faq_bp.route('/faqs/', methods=['GET'])
def faq(lang=None):
    try:
        lang = request.args.get("lang")
        if lang and lang not in LANGUAGES:
            raise ValueError("Invalid Language")
        
        if db.get_translated_lang()==lang:
            faqs = db.get_all_faqs(lang)
        elif lang:
            translate_all_faqs(lang)
    
        faqs = db.get_all_faqs(lang)
        resp = {"faqs": faqs}
        status = STATUS["OK"]

    except ValueError as e:
        resp = IS_ERROR["ERR_FAQ_INVALID_LANG"]
        status = STATUS["BAD_REQUEST"]
        logger.error(f"Invalid Language: {e}")
    
    except Exception as e:
        resp = IS_ERROR["ERR_FAQ_FETCH"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
        logger.error(f"Database Error: {e}")
    
    return jsonify(resp), status


@faq_bp.route('/dummy-data',methods=['POST'])
def dummy():
    try:
        faq_list = [
                {
                    "question": "What is FAQify?",
                    "answer": "FAQify is a simple FAQ application that allows you to view and manage FAQs."
                },
                {
                    "question": "How do I use FAQify?",
                    "answer": "You can view the list of FAQs by visiting the /faq endpoint. You can also add new FAQs by sending a POST request to the /faq endpoint with the question and answer in the request body."
                },
                {
                    "question": "What technologies are used in FAQify?",
                    "answer": "FAQify is built using Python, Flask, and PostgreSQL."
                }
            ]
        head = {
            "Content-Type": "application/json"
        }
        for faq in faq_list:
            redirect_url = request.url.replace("dummy-data", "create-faq")
            resp = requests.post(redirect_url,headers=head, json=faq)
            if resp.status_code != 200:
                raise
        resp = IS_SUCCESS["FAQ_CREATED"]
        status = STATUS["OK"]
    
    except Exception as e:
        resp = IS_ERROR["ERR_FAQ_CREATE"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
        logger.error(f"Database Error: {e}")
    
    return jsonify(resp), status

