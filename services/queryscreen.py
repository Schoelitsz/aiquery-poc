import os
import pyodbc
from flask import Blueprint
from dotenv import load_dotenv

load_dotenv()

queryscreen_bp = Blueprint('queryscreen', __name__)

