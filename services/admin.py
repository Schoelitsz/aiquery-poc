import os
import pyodbc
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

system_connection_string = os.getenv("DB_SYSTEM_CONNECTION_STRING")

