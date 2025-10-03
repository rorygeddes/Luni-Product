"""
Vercel serverless function entry point for Luni Web application.
This file serves as the main entry point for Vercel deployment.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, flash
from src.models.transaction_model import EnhancedTransactionManager, Transaction
from src.parsers.ai_parser import EnhancedAITransactionParser, AITransaction
from config.settings import config
try:
    from src.parsers.plaid_parser import PlaidTransactionParser, PlaidTransaction
    PLAID_AVAILABLE = True
except ImportError:
    PLAID_AVAILABLE = False
    print("Plaid parser not available - install plaid-python and set credentials")
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import tempfile
import json

# Initialize Flask app with configuration
app = Flask(__name__, template_folder='templates')
app.config.from_object(config['production'])

# Initialize managers
transaction_manager = EnhancedTransactionManager()
ai_parser = EnhancedAITransactionParser()

# Global storage for AI transactions and extracted texts
ai_transactions = []
extracted_texts = []

# Global storage for Plaid transactions
plaid_transactions_list = []
plaid_parser = None

# Configure upload settings for Vercel
UPLOAD_FOLDER = '/tmp/uploads'  # Vercel uses /tmp for temporary files
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
AI_ALLOWED_EXTENSIONS = app.config['AI_ALLOWED_EXTENSIONS']

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_ai_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in AI_ALLOWED_EXTENSIONS

# Import all routes from the main app
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard with statistics and roommate balances."""
    try:
        # Get statistics
        stats = transaction_manager.get_statistics()
        
        # Get recent transactions
        recent_transactions = transaction_manager.get_recent_transactions(limit=5)
        
        # Get roommate balances
        roommate_balances = transaction_manager.get_roommate_balances()
        
        return render_template('dashboard.html', 
                             stats=stats,
                             recent_transactions=recent_transactions,
                             roommate_balances=roommate_balances)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html', 
                             stats={},
                             recent_transactions=[],
                             roommate_balances=[])

@app.route('/upload')
def upload():
    """File upload page."""
    return render_template('upload.html')

@app.route('/all_transactions')
def all_transactions():
    """Display all transactions."""
    try:
        transactions = transaction_manager.get_all_transactions()
        return render_template('all_transactions.html', transactions=transactions)
    except Exception as e:
        flash(f'Error loading transactions: {str(e)}', 'error')
        return render_template('all_transactions.html', transactions=[])

@app.route('/plaid_transactions')
def plaid_transactions():
    """Plaid transactions page."""
    return render_template('plaid_transactions.html')

@app.route('/information')
def information():
    """Information page."""
    return render_template('information.html')

@app.route('/input_transaction')
def input_transaction():
    """Manual transaction input page."""
    return render_template('input_transaction.html')

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for dashboard statistics."""
    try:
        stats = transaction_manager.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
