"""
Root entry point for Vercel deployment
"""
import sys
import os

# Add the api directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

# Import and run the Flask app from api/index.py
from api.index import app

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
