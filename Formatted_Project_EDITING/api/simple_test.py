"""
Simple test for Vercel deployment
"""
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from index import app
    print("✅ Flask app imported successfully")
    print("✅ App name:", app.name)
    print("✅ Template folder:", app.template_folder)
    print("✅ Routes:")
    for rule in app.url_map.iter_rules():
        print(f"  - {rule.rule} -> {rule.endpoint}")
    
    # Test a simple route
    with app.test_client() as client:
        response = client.get('/')
        print(f"✅ Root route status: {response.status_code}")
        
        response = client.get('/dashboard')
        print(f"✅ Dashboard route status: {response.status_code}")
        
except Exception as e:
    print("❌ Error:", str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)
