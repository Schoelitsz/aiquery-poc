import os
import pyodbc
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

queryscreen_routes_bp = Blueprint('query_screen', __name__)
# Get the connection string from the environment
system_connection_string = os.getenv("DB_SYSTEM_CONNECTION_STRING")

@queryscreen_routes_bp.route('/query_screen/<int:profile_id>')
def query_screen(profile_id):
    try:
        # Render the query screen with the profile's information
        conn = pyodbc.connect(system_connection_string)
        cursor = conn.cursor()
        
        # Fetch profile details based on profile_id
        cursor.execute('SELECT * FROM profiles where profile_id = ?', profile_id)
        profile = cursor.fetchone()
        conn.close()

        return render_template('queryscreen.html', profile=profile)
    except Exception as e:
        return f"An error occurred: {e}"


@queryscreen_routes_bp.route('/query', methods=['POST'])
def query():
    try:
        # Retrieve the written query
        query = request.form.get('queryinput')
        profile_connection_string = request.form.get('profile_connection_string')
        
        # Create connection and make the query
        conn = pyodbc.connect(profile_connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Fetch all results
        result = cursor.fetchall()
        
        # Convert result to a list of dictionaries
        result_list = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
        
        conn.close()
        
        # Return the result as JSON
        return jsonify({"result": result_list})  # Return as a list of objects

    except Exception as e:
        return jsonify({"error": str(e)})  # Return error as JSON

