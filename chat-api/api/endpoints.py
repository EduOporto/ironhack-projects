from app import app
from flask import request
from sqlalchemy import create_engine
from getpass import getpass
from dotenv import load_dotenv
from bson import json_util
import os

@app.route("/")
def hello_world():
    return {'hello':'world'}


