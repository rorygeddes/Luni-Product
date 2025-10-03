"""
Vercel serverless function entry point for Luni Web application.
This file serves as the main entry point for Vercel deployment.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import os
import json
from datetime import datetime

# Initialize Flask app with configuration
# Try multiple template folder paths for Vercel
template_folders = ['../templates', 'templates', './templates', '/tmp/templates']
template_folder = None

for folder in template_folders:
    if os.path.exists(folder):
        template_folder = folder
        break

if template_folder:
    app = Flask(__name__, template_folder=template_folder)
    print(f"✅ Using template folder: {template_folder}")
else:
    app = Flask(__name__)
    print("⚠️ No template folder found, using default")

# Basic configuration for Vercel
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = False

# Simple transaction storage (in production, use a database)
transactions = []

@app.route('/')
def index():
    """Root route - redirect to dashboard"""
    print("🔍 Root route accessed")
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    print("🔍 Dashboard route accessed")
    try:
        # Simple statistics for demo
        stats = {
            'total_transactions': len(transactions),
            'total_amount': sum(t.get('amount', 0) for t in transactions),
            'recent_count': min(5, len(transactions))
        }
        
        # Get recent transactions
        recent_transactions = transactions[-5:] if transactions else []
        
        print(f"🔍 Attempting to render dashboard.html")
        print(f"🔍 Template folder: {app.template_folder}")
        print(f"🔍 Current directory: {os.getcwd()}")
        
        return render_template('dashboard.html', 
                             stats=stats,
                             recent_transactions=recent_transactions,
                             roommate_balances=[])
    except Exception as e:
        print(f"❌ Template error: {str(e)}")
        # If template fails, return simple HTML
        return f"""
        <html>
        <head><title>Luni Web - Dashboard</title></head>
        <body>
            <h1>Welcome to Luni Web</h1>
            <p>Dashboard is loading...</p>
            <p>Template Error: {str(e)}</p>
            <p>Template folder: {app.template_folder}</p>
            <p>Current directory: {os.getcwd()}</p>
            <nav>
                <a href="/upload">Upload</a> | 
                <a href="/all_transactions">All Transactions</a> | 
                <a href="/information">Information</a>
            </nav>
        </body>
        </html>
        """

@app.route('/upload')
def upload():
    """File upload page"""
    try:
        return render_template('upload.html')
    except Exception as e:
        return f"""
        <html>
        <head><title>Luni Web - Upload</title></head>
        <body>
            <h1>Upload Files</h1>
            <p>Upload functionality coming soon...</p>
            <p>Error: {str(e)}</p>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        """

@app.route('/all_transactions')
def all_transactions():
    """Display all transactions"""
    try:
        return render_template('all_transactions.html', transactions=transactions)
    except Exception as e:
        return f"""
        <html>
        <head><title>Luni Web - All Transactions</title></head>
        <body>
            <h1>All Transactions</h1>
            <p>Transactions: {len(transactions)}</p>
            <p>Error: {str(e)}</p>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        """

@app.route('/plaid_transactions')
def plaid_transactions():
    """Plaid transactions page"""
    try:
        return render_template('plaid_transactions.html')
    except Exception as e:
        return f"""
        <html>
        <head><title>Luni Web - Plaid</title></head>
        <body>
            <h1>Plaid Integration</h1>
            <p>Bank integration coming soon...</p>
            <p>Error: {str(e)}</p>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        """

@app.route('/information')
def information():
    """Information page"""
    try:
        return render_template('information.html')
    except Exception as e:
        return f"""
        <html>
        <head><title>Luni Web - Information</title></head>
        <body>
            <h1>Information</h1>
            <p>App information...</p>
            <p>Error: {str(e)}</p>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        """

@app.route('/input_transaction')
def input_transaction():
    """Manual transaction input page"""
    try:
        return render_template('input_transaction.html')
    except Exception as e:
        return f"""
        <html>
        <head><title>Luni Web - Input Transaction</title></head>
        <body>
            <h1>Input Transaction</h1>
            <p>Manual transaction entry...</p>
            <p>Error: {str(e)}</p>
            <a href="/dashboard">Back to Dashboard</a>
        </body>
        </html>
        """

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for dashboard statistics"""
    try:
        stats = {
            'total_transactions': len(transactions),
            'total_amount': sum(t.get('amount', 0) for t in transactions),
            'recent_count': min(5, len(transactions))
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel handler - this is what Vercel calls
def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)