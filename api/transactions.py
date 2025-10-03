"""
API endpoint for Luni Web transactions
"""
from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage (in production, use a database)
transactions = [
    {
        "id": 1,
        "date": "2024-10-03",
        "description": "Coffee Shop",
        "amount": -4.50,
        "category": "Food & Dining"
    },
    {
        "id": 2,
        "date": "2024-10-03",
        "description": "Grocery Store",
        "amount": -85.30,
        "category": "Groceries"
    },
    {
        "id": 3,
        "date": "2024-10-02",
        "description": "Salary Deposit",
        "amount": 3000.00,
        "category": "Income"
    }
]

@app.route('/api/transactions')
def get_transactions():
    """Get all transactions"""
    return jsonify({
        "transactions": transactions,
        "total": len(transactions),
        "status": "success"
    })

@app.route('/api/statistics')
def get_statistics():
    """Get dashboard statistics"""
    total_amount = sum(t['amount'] for t in transactions)
    recent_count = len([t for t in transactions if t['date'] >= '2024-10-01'])
    
    return jsonify({
        "total_transactions": len(transactions),
        "total_amount": total_amount,
        "recent_count": recent_count,
        "success_rate": 100,
        "status": "success"
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    # In a real implementation, you would process the uploaded file
    return jsonify({
        "message": "File uploaded successfully",
        "status": "success"
    })

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
