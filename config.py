import os
from datetime import datetime

# This config.py file will create new settings what can be passed to Flask app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.abspath('applications/content/html/')
static_folder = os.path.abspath('applications/content/')

# Base page auto generated values
date_rng = '2021' if datetime.now().year == 2021 else f'2021 - {datetime.now().year}'
_auto_values = {
    'author': 'GhosterSK',
    'dates_rng': date_rng
    }

# Change current_mode to what mode you want run the app
# *****************************************************
current_mode = 'config.DevelopmentConfig'
# *****************************************************


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "Xfh5-1$-tHe-d3fault-k€y")
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY", 'th1s-iS-n0T-r@n0Om-b*t-it-should-be')
    
    UPLOAD_FOLDER = os.path.abspath('applications/content/upl_files/')
    ALLOWED_EXTENSIONS = {'text': ['txt', 'pdf', 'doc', 'docx', 'csv', 'xls',
                        'xlsx'], 'excel': ['csv', 'xls', 'xlsx'],
                        'image': ['png', 'jpg', 'jpeg', 'gif']}

    database_engine = None
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'base_dtb.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    THREADS_PER_PAGE = 2

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.getenv("CSRF_SESSION_KEY", "Xfh5-1$-tHe-d3fault-k€y")


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
