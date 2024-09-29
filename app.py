import os
import pyodbc
from flask import Flask, redirect, url_for, render_template, request
from dotenv import load_dotenv
from routes.admin_routes import admin_routes_bp
from routes.manageprofiles_routes import manageprofiles_routes_bp
from routes.queryscreen_routes import queryscreen_routes_bp
from routes.profiledetails_routes import profiledetails_routes_bp
from routes.newprofiles_routes import newprofiles_routes_bp
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.secret_key = os.urandom(24) 


# Get the connection string from the environment
system_connection_string = os.getenv("DB_SYSTEM_CONNECTION_STRING")
app.register_blueprint(admin_routes_bp)
app.register_blueprint(manageprofiles_routes_bp)
app.register_blueprint(queryscreen_routes_bp)
app.register_blueprint(profiledetails_routes_bp)
app.register_blueprint(newprofiles_routes_bp)


def get_db_connection():
    try:
        # Establish a database connection using pyodbc
        conn = pyodbc.connect(system_connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise e


@app.route('/')
def home():
    try:
       
        conn = pyodbc.connect(system_connection_string)
        cursor = conn.cursor()
        
        # Fetch profiles from the database
        cursor.execute('SELECT profile_id, profile_name FROM profiles')
        profiles = cursor.fetchall()
        conn.close()
        return render_template('index.html', profiles=profiles)
    except Exception as e:
        return f"An error occurred: {e}"
    

@app.route('/loadchatforprofile', methods=['POST'])
def loadchatforprofile():
    profile_id = request.form['profile_id']
    return redirect(url_for('query_screen.query_screen', profile_id=profile_id))


if __name__ == '__main__':
    app.run(debug=True)
