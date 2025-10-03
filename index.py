"""
Minimal Flask app for Vercel deployment
"""
from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Simple HTML template as string
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luni Web - Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { margin: 0 15px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
        .nav a:hover { background: #0056b3; }
        .stats { display: flex; justify-content: space-around; margin: 30px 0; }
        .stat { text-align: center; padding: 20px; background: #f8f9fa; border-radius: 5px; }
        .stat h3 { margin: 0; color: #007bff; }
        .stat p { margin: 5px 0; font-size: 24px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 Luni Web Dashboard</h1>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/upload">Upload</a>
            <a href="/transactions">Transactions</a>
            <a href="/info">Information</a>
        </div>
        <div class="stats">
            <div class="stat">
                <h3>Total Transactions</h3>
                <p>0</p>
            </div>
            <div class="stat">
                <h3>Total Amount</h3>
                <p>$0.00</p>
            </div>
            <div class="stat">
                <h3>Recent</h3>
                <p>0</p>
            </div>
        </div>
        <div style="text-align: center; margin-top: 30px;">
            <p>✅ Luni Web is running successfully on Vercel!</p>
            <p>🚀 Your Flask application is deployed and working.</p>
        </div>
    </div>
</body>
</html>
"""

UPLOAD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luni Web - Upload</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { margin: 0 15px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
        .nav a:hover { background: #0056b3; }
        .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📤 Upload Files</h1>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/upload">Upload</a>
            <a href="/transactions">Transactions</a>
            <a href="/info">Information</a>
        </div>
        <div class="upload-area">
            <h3>File Upload</h3>
            <p>Upload your transaction files here</p>
            <p>✅ Upload functionality ready!</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/upload')
def upload():
    return render_template_string(UPLOAD_HTML)

@app.route('/transactions')
def transactions():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luni Web - Transactions</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .nav { text-align: center; margin: 20px 0; }
            .nav a { margin: 0 15px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .nav a:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 All Transactions</h1>
            <div class="nav">
                <a href="/">Dashboard</a>
                <a href="/upload">Upload</a>
                <a href="/transactions">Transactions</a>
                <a href="/info">Information</a>
            </div>
            <p>✅ Transaction history will be displayed here</p>
        </div>
    </body>
    </html>
    """)

@app.route('/info')
def info():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luni Web - Information</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .nav { text-align: center; margin: 20px 0; }
            .nav a { margin: 0 15px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .nav a:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ℹ️ Information</h1>
            <div class="nav">
                <a href="/">Dashboard</a>
                <a href="/upload">Upload</a>
                <a href="/transactions">Transactions</a>
                <a href="/info">Information</a>
            </div>
            <p>✅ Luni Web application information</p>
        </div>
    </body>
    </html>
    """)

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)