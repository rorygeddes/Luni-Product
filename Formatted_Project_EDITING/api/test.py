"""
Test script for Vercel deployment
"""
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from index import app
    print("✅ Flask app imported successfully")
    print("✅ App name:", app.name)
    print("✅ Template folder:", app.template_folder)
    print("✅ Routes:", [rule.rule for rule in app.url_map.iter_rules()])
except Exception as e:
    print("❌ Error importing Flask app:", str(e))
    sys.exit(1)
