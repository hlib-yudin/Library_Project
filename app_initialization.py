from flask_sqlalchemy import SQLAlchemy
from flask import Flask, make_response, render_template, url_for, request, redirect, jsonify,json, flash, session
from flask_session import Session
# from config import Config
from dateutil.relativedelta import *
import json
import os
import psycopg2
from config import configurate

#
app = Flask(__name__, template_folder='boostrap/Pages')
configurate(app)
# app.config.from_object(Config)


# SQLALCHEMY_TRACK_MODIFICATIONS = 'False'


Session(app)

db = SQLAlchemy(app)
db.init_app(app)
