import os
import pyodbc
from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv

profiledetails_routes_bp = Blueprint('profiledetails', __name__)

# Load environment variables from .env file
load_dotenv()
system_connection_string = os.getenv("DB_SYSTEM_CONNECTION_STRING")

@profiledetails_routes_bp.route('/profiledetails/<int:profile_id>')
def profiledetails(profile_id):
    try:
        conn = pyodbc.connect(system_connection_string)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM profiles WHERE profile_id = ?', (profile_id,))
        profile = cursor.fetchone()
        conn.close()

        return render_template('profiledetails.html', profile=profile)
    except Exception as e:
        return f"An error occurred: {e}"
    

@profiledetails_routes_bp.route('/profiledetails/<int:profile_id>/save', methods=['POST'])
def saveprofile(profile_id):
    try:
        # Retrieve form data
        profile_name = request.form.get('profile_name')
        db_connection_info = request.form.get('db_connection_info')
        abstract_layer_path = request.form.get('abstract_layer_path')
    
        # Connect to the database
        conn = pyodbc.connect(system_connection_string)
        cursor = conn.cursor()

        # Update the existing profile
        cursor.execute('''
            UPDATE profiles
            SET profile_name = ?, db_connection_info = ?, abstract_layer_path = ?
            WHERE profile_id = ?
        ''', (profile_name, db_connection_info, abstract_layer_path, profile_id))

        conn.commit()
        conn.close()

        flash('Profile updated successfully!', 'success')  # Flash message for user feedback
        return redirect(url_for('profiledetails.profiledetails', profile_id=profile_id))
    
    except Exception as e:
        return f"An error occurred while saving the profile: {e}"

@profiledetails_routes_bp.route('/delete/<int:profile_id>', methods=['POST'])
def delete_profile(profile_id):
    try:
        conn = pyodbc.connect(system_connection_string)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM profiles WHERE profile_id = ?', (profile_id,))
        conn.commit()
        conn.close()
        return redirect('/')
    except Exception as e:
        return f"An error occurred while deleting the profile: {e}"
