# settings.py - Application Configuration

## 📋 File Purpose
- **Centralized Configuration**: All application settings in one place
- **Environment Management**: Handles different environments (dev/prod)
- **Security Settings**: Manages API keys and sensitive configuration
- **Feature Flags**: Controls application features and behavior

## 🔧 Core Functionality
- **Environment Variables**: Loads configuration from .env file
- **API Key Management**: Securely handles OpenAI and Plaid API keys
- **File Upload Settings**: Configures file size limits and allowed types
- **Security Configuration**: Sets up Flask security settings

## 📊 Key Classes
- **Config**: Base configuration class with common settings
- **DevelopmentConfig**: Development-specific settings
- **ProductionConfig**: Production-specific settings
- **config**: Dictionary mapping environments to configuration classes

## 🔄 Recent Updates
- **2024-10-03**: Created new centralized configuration system
- **2024-10-03**: Moved all hardcoded settings to configuration file
- **2024-10-03**: Added environment-based configuration support
- **2024-10-03**: Improved security with centralized API key management

## 🎯 Configuration Options
- **Flask Settings**: Secret key, debug mode, host, port
- **API Keys**: OpenAI, Plaid client ID and secret
- **File Upload**: Max file size, allowed extensions
- **Data Files**: Transaction file path and settings

## 🔧 Environment Variables
- **SECRET_KEY**: Flask secret key for sessions
- **FLASK_DEBUG**: Debug mode setting
- **OPENAI_API_KEY**: OpenAI API key for AI parsing
- **PLAID_CLIENT_ID**: Plaid client ID for bank integration
- **PLAID_SECRET**: Plaid secret for bank integration
- **PLAID_ENVIRONMENT**: Plaid environment (sandbox/production)

## 🚀 Benefits
- **Centralized Management**: All settings in one place
- **Environment Support**: Different settings for dev/prod
- **Security**: Secure handling of sensitive data
- **Flexibility**: Easy to modify settings without code changes

## 🔑 Security Features
- **Environment Variables**: Sensitive data not in code
- **API Key Protection**: Secure storage of API keys
- **File Upload Limits**: Prevents abuse and security issues
- **Debug Mode Control**: Disable debug in production
