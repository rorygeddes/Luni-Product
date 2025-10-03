# vercel.json - Vercel Deployment Configuration

## 📋 File Purpose
- **Deployment Configuration**: Configures how the application is deployed on Vercel
- **Serverless Setup**: Defines serverless function configuration
- **Routing Rules**: Maps all requests to the Flask application
- **Environment Settings**: Sets production environment variables

## 🔧 Core Functionality
- **Build Configuration**: Defines how Vercel builds the application
- **Function Setup**: Configures serverless function behavior
- **Route Mapping**: Routes all requests to the Flask app
- **Environment Variables**: Sets production environment settings

## 📊 Key Configuration
- **Version**: Vercel configuration version 2
- **Builds**: Uses @vercel/python for Python applications
- **Routes**: All requests (.*) routed to app.py
- **Environment**: Sets FLASK_ENV to production
- **Functions**: 30-second timeout for serverless functions

## 🔄 Recent Updates
- **2024-10-03**: Created Vercel configuration for automatic deployment
- **2024-10-03**: Set up serverless function configuration
- **2024-10-03**: Configured routing for Flask application
- **2024-10-03**: Added production environment settings

## 🎯 Configuration Details
- **Build Source**: Points to app.py as the main application
- **Python Runtime**: Uses Vercel's Python runtime
- **Request Routing**: All HTTP requests go to Flask app
- **Function Timeout**: 30 seconds for serverless execution

## 🚀 Deployment Benefits
- **Automatic Deployment**: Deploys on every GitHub push
- **Serverless**: No server management required
- **Global CDN**: Fast loading worldwide
- **SSL Certificate**: Automatic HTTPS
- **Custom Domains**: Easy custom domain setup

## 🔧 Environment Variables
- **FLASK_ENV**: Set to production for Vercel
- **OPENAI_API_KEY**: Required for AI functionality
- **SECRET_KEY**: Flask secret key for sessions
- **PLAID_***: Optional bank integration variables
