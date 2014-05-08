import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATA_DIR = os.path.join(ROOT_DIR, 'data')
DB_NAME = 'twitter_db.db'
DB_PATH = os.path.join(DATA_DIR, DB_NAME)


CONF_DIR = os.path.join(ROOT_DIR, 'conf')
SRC_DIR = os.path.join(ROOT_DIR, 'twitter_rec')
