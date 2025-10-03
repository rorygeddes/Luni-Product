# vercel_app.py - Vercel-Optimized Flask Application

## 📋 File Purpose
- **Vercel Deployment**: Optimized Flask app for Vercel serverless deployment
- **Production Ready**: Configured for production environment
- **Serverless Optimized**: Uses /tmp for file storage (Vercel requirement)
- **Simplified Routes**: Core routes for serverless deployment

## 🔧 Core Functionality
- **Production Configuration**: Uses production settings from config
- **Temporary Storage**: Uses /tmp/uploads for file uploads (Vercel requirement)
- **Core Routes**: Essential routes for application functionality
- **Error Handling**: Robust error handling for serverless environment

## 📊 Key Features
- **Serverless Compatible**: Optimized for Vercel's serverless functions
- **File Upload Handling**: Uses /tmp directory for temporary files
- **Production Settings**: Configured for production deployment
- **Simplified Structure**: Core functionality without development features

## 🔄 Recent Updates
- **2024-10-03**: Created Vercel-optimized Flask application
- **2024-10-03**: Configured for serverless deployment
- **2024-10-03**: Set up /tmp file storage for Vercel
- **2024-10-03**: Added production environment configuration

## 🎯 Key Routes
- `/` → Redirects to dashboard
- `/dashboard` → Main application dashboard
- `/api/statistics` → API endpoint for dashboard data

## 🔧 Vercel-Specific Features
- **Temporary Storage**: Uses /tmp/uploads for file uploads
- **Production Config**: Uses production configuration settings
- **Serverless Handler**: Compatible with Vercel's serverless functions
- **Environment Variables**: Reads from Vercel environment

## 🚀 Deployment Benefits
- **Automatic Scaling**: Scales automatically with traffic
- **Global Distribution**: Deployed to Vercel's global network
- **Zero Server Management**: No server maintenance required
- **Cost Effective**: Pay only for actual usage

## 💡 Key Differences from app.py
- **Simplified Routes**: Only core routes for production
- **Production Config**: Uses production settings
- **Temporary Storage**: Uses /tmp instead of local uploads
- **Serverless Optimized**: Configured for serverless deployment
