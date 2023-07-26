import sys
sys.path.append("./")
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

db = SQLAlchemy(app)

class StarUser(db.Model):
    __tablename__ = 'tb_staruser'
    pk = Column(Integer, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    media_count = Column(Integer)
    follower_count = Column(Integer)
    following_count = Column(Integer)
    external_url = Column(String)
    public_email = Column(String)
    city = Column(String)


