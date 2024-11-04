# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha_chave_secreta'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://postgres:1234@localhost/T2-BAN2'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://gio:manaluiza1304@localhost/pousada'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
