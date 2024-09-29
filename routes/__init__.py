from flask import Flask
from routes.queryscreen_routes import queryscreen_routes_bp
#from routes.admin_routes import admin_routes_bp
#from services.run_query import query_api_bp
#from phivenv import get_db_connection

#connectionstring = get_db_connection
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(queryscreen_routes_bp)
#app.register_blueprint(admin_routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
