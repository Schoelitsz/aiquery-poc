import os
import pyodbc
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from routes.profiledetails_routes import profiledetails_routes_bp
from dotenv import load_dotenv

manageprofiles_routes_bp = Blueprint('manageprofiles', __name__)

# Load environment variables from .env file
load_dotenv()
system_connection_string = os.getenv("DB_SYSTEM_CONNECTION_STRING")

manageprofiles_routes_bp.register_blueprint(profiledetails_routes_bp)

@manageprofiles_routes_bp.route('/manageprofiles')
def manageprofiles():
    try:
        conn = pyodbc.connect(system_connection_string)
        cursor = conn.cursor()
        cursor.execute('Select * from profiles')
        profiles = cursor.fetchall()
        conn.close()

        return render_template('manageprofiles.html', profiles=profiles)
    except Exception as e:
        return f"An error occurred: {e}"
    

@manageprofiles_routes_bp.route('/details', methods=['POST']) #slash is the action of the form
def profiledetails():
    profile_id = request.form['chosenprofile']
    return redirect(url_for('profiledetails.profiledetails', profile_id=profile_id))