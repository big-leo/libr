from flask import Flask
from flask.ext.login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)

from mainapp import views, models
Base.metadata.create_all(bind=engine)
