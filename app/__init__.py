from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .routes import faq_bp
    app.register_blueprint(faq_bp)
    return app
