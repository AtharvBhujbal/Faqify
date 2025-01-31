from flask import Blueprint, render_template

faq_bp = Blueprint('faq', __name__)

@faq_bp.route('/')
def hello():
    return render_template('index.html')