import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Configure the database - use SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data', 'printing_costs.db')}"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Initialize the app with the extension
    db.init_app(app)
    
    # إضافة فلاتر جينجا للتعامل مع التوقيت المصري
    from utils import format_cairo_datetime, format_relative_time
    
    @app.template_filter('cairo_datetime')
    def cairo_datetime_filter(datetime_obj, format_string='%Y-%m-%d %H:%M'):
        """فلتر لتنسيق التاريخ والوقت بتوقيت القاهرة"""
        return format_cairo_datetime(datetime_obj, format_string)
    
    @app.template_filter('relative_time')
    def relative_time_filter(datetime_obj):
        """فلتر لعرض الوقت النسبي بالعربية"""
        return format_relative_time(datetime_obj)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)