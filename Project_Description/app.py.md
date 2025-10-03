# app.py - Main Flask Application

## 📋 File Purpose
- **Main Entry Point**: The core Flask web application that handles all HTTP requests
- **Route Handler**: Defines all URL endpoints and their corresponding functions
- **File Upload Manager**: Handles file uploads for AI parsing and CSV imports
- **Session Manager**: Manages user sessions and flash messages

## 🔧 Core Functionality
- **Web Server**: Serves the application on port 3000
- **API Endpoints**: Provides REST API for AJAX requests
- **File Processing**: Handles image/PDF uploads for AI parsing
- **Data Management**: Manages transaction data and roommate balances

## 📊 Key Components
- **Flask App Initialization**: Sets up the web server with configuration
- **Route Definitions**: Maps URLs to Python functions
- **File Upload Handling**: Processes uploaded files for AI analysis
- **Data Persistence**: Saves and loads transaction data from JSON

## 🔄 Recent Updates
- **2024-10-03**: Added Vercel deployment configuration and optimization
- **2024-10-03**: Created vercel_app.py for serverless deployment
- **2024-10-03**: Added Vercel-specific requirements and build scripts
- **2024-10-03**: Reorganized imports to use new modular structure
- **2024-10-03**: Updated to use centralized configuration from config/settings.py
- **2024-10-03**: Changed default port from 3001 to 3000
- **2024-10-03**: Improved error handling and file validation

## 🎯 Key Routes
- `/` → Redirects to dashboard
- `/dashboard` → Main application dashboard
- `/upload` → File upload interface
- `/all_transactions` → Transaction management
- `/plaid_transactions` → Bank integration
- `/input_transaction` → Manual transaction entry

## 🔧 Dependencies
- Flask framework
- OpenAI API integration
- Plaid API integration
- File upload handling
- JSON data persistence
