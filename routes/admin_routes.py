import os
import pyodbc
from flask import Blueprint, render_template
from dotenv import load_dotenv


admin_routes_bp = Blueprint('admin_routes', __name__)

# Load environment variables from .env file
load_dotenv()
system_connection_string = os.getenv("DB_SYSTEM_CONNECTION_STRING")


def get_db_connection():
    try:
        # Establish a database connection using pyodbc
        conn = pyodbc.connect(system_connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise e

@admin_routes_bp.route('/admin')
def admin():
    try:
        conn = pyodbc.connect(system_connection_string)
        cursor = conn.cursor()
        #fetch the test table
        cursor.execute('SELECT * from test')
        test = cursor.fetchall()
        #fetch the connectionstring for profile 1(phi phi)
        cursor.execute('Select db_connection_info from profiles where profile_id = 1')
        result = cursor.fetchone()

        if result:
            connectionstring_profile = result[0]  # Extract the connection string from the tuple
        else:
            return "Profile not found", 404
        
        conn.close()

        conn2 = pyodbc.connect(connectionstring_profile)
        cursor2 = conn2.cursor()
        cursor2.execute('select * from patients')
        patients = cursor2.fetchall()
        conn2.close()
        return render_template('admin.html', test=test, connectionstring=connectionstring_profile, patients=patients)
    except Exception as e:
            return f"An error occurred: {e}"
