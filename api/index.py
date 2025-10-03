from app import app

# This is the entry point for Vercel
# It imports your main Flask app from app.py
# Vercel will use this as the serverless function entry point

if __name__ == '__main__':
    app.run(debug=True)