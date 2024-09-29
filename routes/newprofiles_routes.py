import os
import datetime
import pyodbc
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

newprofiles_routes_bp = Blueprint('newprofile', __name__)

# Load environment variables from .env file
load_dotenv()
system_connection_string = os.getenv("DB_SYSTEM_CONNECTION_STRING")

# Helper function to test the database connection
def test_connection(connection_string):
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        # Try a simple query to test the connection
        cursor.execute("SELECT 1")
        conn.close()
        return True
    except Exception as e:
        return str(e)  # Return the error message if the connection fails

@newprofiles_routes_bp.route('/newprofile', methods=['GET'])
def newprofiles():
    current_date = datetime.date.today().isoformat()
    return render_template('newprofiles.html', date=current_date)

@newprofiles_routes_bp.route('/savenewprofile', methods=['POST'])  # Accept POST requests
def savenewprofile():
    try:
        # Retrieve form data
        name = request.form.get('profile_name')
        connection_string = request.form.get('db_connection_info')
        layerpath = request.form.get('abstract_layer_path')
        date = request.form.get('created_at')

        # Test the connection before saving the profile
        connection_test_result = test_connection(connection_string)
        
        if connection_test_result is True:
            # Connection successful, proceed with saving the profile
            conn = pyodbc.connect(system_connection_string)
            cursor = conn.cursor()

            # Correct SQL syntax for INSERT statement
            cursor.execute('''
                INSERT INTO profiles (profile_name, db_connection_info, abstract_layer_path, created_at)
                VALUES (?, ?, ?, ?)
            ''', (name, connection_string, layerpath, date))

            conn.commit()
            conn.close()

            flash('Profile created and connection is valid!', 'success')  # Flash success message
            return redirect(url_for('newprofile.newprofiles'))  # Ensure this is the correct endpoint
        else:
            # Connection test failed, flash error message
            flash(f'Connection test failed: {connection_test_result}', 'danger')
            return redirect(url_for('newprofile.newprofiles'))  # Redirect back to profile creation page
    except Exception as e:
        flash(f'An error occurred while saving the profile: {e}', 'danger')  # Use flash for general error
        return redirect(url_for('newprofile.newprofiles'))  # Redirect back to profile creation page
