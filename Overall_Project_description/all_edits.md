# Luni Web - Complete Project Documentation for ChatGPT

## 📋 Project Overview
This document contains the complete technical documentation of the Luni Web application - a Flask-based transaction management system with AI-powered receipt parsing and roommate expense tracking. This document is designed to provide ChatGPT with comprehensive understanding of the entire codebase, architecture, and functionality.

## 🏗️ Project Architecture

### **Main Application Structure**
```
Formatted_Project_EDITING/          # Working application files
├── app.py                         # Main Flask application (829 lines)
├── requirements.txt               # Python dependencies
├── setup.py                      # Automated setup script
├── README.md                      # Comprehensive documentation
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
├── transactions.json              # Data persistence (353 lines)
├── src/                          # Source code modules
│   ├── models/
│   │   └── transaction_model.py  # Data models and business logic (667 lines)
│   ├── parsers/
│   │   ├── ai_parser.py          # AI-powered parsing (399 lines)
│   │   └── plaid_parser.py       # Bank integration (260 lines)
│   └── utils/                    # Utility functions
├── config/
│   └── settings.py               # Application configuration
├── templates/                    # HTML templates
│   ├── base.html                 # Base template with navigation
│   ├── dashboard.html            # Main dashboard
│   ├── upload.html               # File upload interface
│   ├── all_transactions.html     # Transaction management
│   ├── plaid_transactions.html   # Bank integration
│   ├── input_transaction.html    # Manual entry
│   └── information.html          # Settings
├── docs/                         # Documentation
└── uploads/                      # File upload directory
```

## 🔧 Core Application Components

### **1. Main Flask Application (app.py - 829 lines)**
**Purpose**: Central web server handling all HTTP requests and application logic.

**Key Functionality**:
- **Web Server**: Serves application on port 3000 with debug mode
- **Route Management**: Handles all URL endpoints and HTTP methods
- **File Upload Processing**: Manages image/PDF uploads for AI parsing
- **Session Management**: Handles user sessions and flash messages
- **API Integration**: Connects to OpenAI and Plaid APIs
- **Data Persistence**: Manages transaction data storage and retrieval

**Key Routes**:
- `/` → Redirects to dashboard
- `/dashboard` → Main application interface with statistics
- `/upload` → File upload interface for AI parsing and CSV import
- `/all_transactions` → Transaction management and editing
- `/plaid_transactions` → Bank account integration
- `/input_transaction` → Manual transaction entry
- `/information` → Settings and configuration

**API Endpoints**:
- `/api/statistics` → Real-time dashboard data
- `/api/upload` → File upload processing
- `/api/parse_ai` → AI-powered transaction extraction
- `/plaid_link_token` → Bank connection tokens

**Recent Updates**:
- **2024-10-03**: Reorganized imports to use modular structure (src/models/, src/parsers/)
- **2024-10-03**: Updated to use centralized configuration from config/settings.py
- **2024-10-03**: Changed default port from 3001 to 3000
- **2024-10-03**: Improved error handling and file validation

### **2. Transaction Model (src/models/transaction_model.py - 667 lines)**
**Purpose**: Core business logic and data management for all transaction operations.

**Key Classes**:
- **EnhancedTransactionManager**: Main class for transaction CRUD operations
- **Transaction**: Data model for individual transactions
- **Roommate**: Manages roommate relationships and balances
- **Account**: Handles spending categories and hierarchies

**Core Functionality**:
- **Transaction Management**: Add, edit, delete, and retrieve transactions
- **Balance Calculations**: Computes who owes what to whom
- **Data Validation**: Ensures data integrity and consistency
- **Roommate Management**: Tracks roommate relationships and balances
- **Account Management**: Manages spending categories and sub-accounts
- **Data Persistence**: Saves and loads data from JSON files

**Key Methods**:
- `add_transaction()`: Adds new transactions with validation
- `get_transactions()`: Retrieves transactions with filtering options
- `calculate_balances()`: Computes net balances for each roommate
- `save_data()`: Persists data to transactions.json
- `load_data()`: Loads data from JSON file
- `update_transaction()`: Modifies existing transactions
- `delete_transaction()`: Removes transactions from system

**Data Structure**:
```python
Transaction = {
    "id": "unique_identifier",
    "amount": 25.50,
    "description": "Grocery shopping",
    "date": "2024-01-15",
    "category": "Food",
    "subcategory": "Groceries",
    "payment_method": "Debit Card",
    "roommate": "John",
    "split_amount": 12.75
}
```

### **3. AI Parser (src/parsers/ai_parser.py - 399 lines)**
**Purpose**: AI-powered transaction extraction from receipts, images, and documents.

**Key Classes**:
- **EnhancedAITransactionParser**: Main parser class for AI processing
- **AITransaction**: Data model for AI-parsed transactions
- **ImageProcessor**: Handles image preprocessing and format conversion
- **TextAnalyzer**: Processes extracted text for transaction data

**Core Functionality**:
- **Image Analysis**: Uses OpenAI Vision API to analyze receipt images
- **Text Extraction**: Extracts text from images, PDFs, and documents
- **Transaction Parsing**: Identifies amounts, dates, and descriptions
- **Smart Categorization**: Automatically assigns spending categories
- **Data Validation**: Ensures parsed data accuracy and completeness

**Supported Formats**:
- **Images**: JPG, PNG, GIF, BMP, WebP, HEIC
- **Documents**: PDF files
- **Receipts**: Various receipt formats and layouts
- **Bank Statements**: Screenshots and scanned statements

**Key Methods**:
- `parse_receipt()`: Main method for parsing receipt images
- `extract_text()`: Extracts text using OpenAI Vision API
- `identify_transactions()`: Finds transaction data in extracted text
- `categorize_transaction()`: Automatically assigns categories
- `validate_data()`: Ensures parsed data is accurate

**AI Features**:
- **Smart Parsing**: Uses AI to understand receipt layouts
- **Amount Detection**: Accurately identifies monetary amounts
- **Date Recognition**: Extracts transaction dates
- **Merchant Identification**: Recognizes store names and locations
- **Category Assignment**: Automatically suggests spending categories

### **4. Plaid Parser (src/parsers/plaid_parser.py - 260 lines)**
**Purpose**: Bank account integration for automatic transaction retrieval.

**Key Classes**:
- **PlaidTransactionParser**: Main parser class for bank integration
- **PlaidTransaction**: Data model for bank transactions
- **AccountManager**: Manages connected bank accounts
- **DataConverter**: Converts bank data to application format

**Core Functionality**:
- **Account Linking**: Connects user bank accounts securely via OAuth
- **Transaction Retrieval**: Fetches recent transactions from banks
- **Data Processing**: Converts bank data to application format
- **Error Handling**: Manages connection issues and API failures

**Supported Banks**:
- **Major Banks**: Chase, Bank of America, Wells Fargo, etc.
- **Credit Unions**: Local and national credit unions
- **Online Banks**: Ally, Capital One 360, etc.
- **International**: Some international banks via Plaid

**Key Methods**:
- `connect_account()`: Establishes secure bank connection
- `fetch_transactions()`: Retrieves transactions from bank
- `process_transactions()`: Converts bank data to application format
- `validate_connection()`: Ensures bank connection is valid

**Security Features**:
- **OAuth Authentication**: Secure bank account access
- **Token Management**: Secure storage of access tokens
- **Data Encryption**: All data encrypted in transit
- **Permission Scoping**: Limited access to transaction data only

### **5. Configuration System (config/settings.py)**
**Purpose**: Centralized application configuration and environment management.

**Key Classes**:
- **Config**: Base configuration class with common settings
- **DevelopmentConfig**: Development-specific settings
- **ProductionConfig**: Production-specific settings

**Configuration Options**:
- **Flask Settings**: Secret key, debug mode, host, port
- **API Keys**: OpenAI, Plaid client ID and secret
- **File Upload**: Max file size (16MB), allowed extensions
- **Data Files**: Transaction file path and settings

**Environment Variables**:
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_DEBUG`: Debug mode setting
- `OPENAI_API_KEY`: OpenAI API key for AI parsing
- `PLAID_CLIENT_ID`: Plaid client ID for bank integration
- `PLAID_SECRET`: Plaid secret for bank integration
- `PLAID_ENVIRONMENT`: Plaid environment (sandbox/production)

## 🎨 Frontend Templates

### **Base Template (templates/base.html)**
**Purpose**: Foundation template providing common layout and navigation.

**Key Components**:
- **Navigation Menu**: Main application navigation with all sections
- **Responsive Design**: Mobile-friendly layout and navigation
- **Common Styling**: Shared CSS and JavaScript
- **Template Blocks**: Defines areas for page-specific content

**Navigation Sections**:
- Dashboard, Upload, All Transactions, Plaid Transactions, Input Transaction, Information

### **Dashboard Template (templates/dashboard.html)**
**Purpose**: Main application interface showing transaction summaries and roommate balances.

**Key Components**:
- **Summary Cards**: Key statistics and metrics
- **Recent Transactions**: Latest transaction entries
- **Roommate Balances**: Current balance status
- **Quick Actions**: Buttons for common tasks
- **Real-time Updates**: Live data and statistics

### **Upload Template (templates/upload.html)**
**Purpose**: File upload interface for AI parsing and CSV import.

**Key Components**:
- **Drag & Drop Upload**: Easy file upload interface
- **File Validation**: Checks file types and sizes
- **AI Processing**: Sends files to AI parser for analysis
- **Progress Tracking**: Shows upload and processing progress

**Supported File Types**:
- **AI Parsing**: Images (JPG, PNG, HEIC), PDFs, receipts
- **CSV Import**: Comma-separated value files
- **File Size**: Up to 16MB per file

## 🔄 Data Flow and Workflow

### **Transaction Processing Workflow**:
1. **User uploads receipt/image** → Upload interface
2. **AI Parser extracts data** → OpenAI Vision API analysis
3. **Transaction Model validates** → Data validation and business logic
4. **Data stored in JSON** → transactions.json persistence
5. **Dashboard updates** → Real-time UI updates
6. **Roommate balances recalculated** → Balance computation

### **Bank Integration Workflow**:
1. **User connects bank account** → Plaid OAuth flow
2. **Plaid retrieves transactions** → Bank API integration
3. **Data converted to app format** → Standardization
4. **Transactions added to system** → Integration with existing data
5. **Balances updated** → Roommate balance recalculation

## 🛠️ Technical Stack

### **Backend Technologies**:
- **Flask**: Web framework and routing
- **Python 3.13**: Programming language
- **OpenAI API**: AI-powered parsing and analysis
- **Plaid API**: Bank account integration
- **Pandas**: Data manipulation and CSV processing
- **Pillow**: Image processing and format conversion

### **Frontend Technologies**:
- **HTML5**: Semantic markup structure
- **CSS3**: Responsive styling and layout
- **JavaScript**: Client-side interactions
- **Jinja2**: Template engine for dynamic content

### **Data Storage**:
- **JSON**: Primary data persistence (transactions.json)
- **File System**: Uploaded files and images
- **Environment Variables**: Configuration and API keys

## 🔐 Security and Configuration

### **Security Features**:
- **Environment Variables**: Sensitive data not in code
- **API Key Protection**: Secure storage of API keys
- **File Upload Validation**: Prevents abuse and security issues
- **Input Sanitization**: Protects against malicious input
- **Session Management**: Secure user session handling

### **Configuration Management**:
- **Centralized Settings**: All configuration in config/settings.py
- **Environment Support**: Different settings for dev/prod
- **API Key Management**: Secure handling of sensitive data
- **File Upload Limits**: Prevents abuse and security issues

## 📊 Key Features and Capabilities

### **AI-Powered Transaction Parsing**:
- Upload receipts, bank statements, screenshots
- Automatic transaction extraction using OpenAI Vision
- Smart categorization and amount detection
- Support for multiple image formats including HEIC

### **Roommate Expense Management**:
- Split expenses between roommates
- Track who owes what to whom
- Balance calculations and notifications
- Hierarchical account management

### **Financial Data Management**:
- Hierarchical account structure
- Multiple payment methods
- Transaction filtering and search
- Real-time dashboard updates

### **Bank Integration (Optional)**:
- Plaid API integration
- Automatic bank transaction sync
- Secure financial data access
- Multi-bank support

## 🚀 Development and Deployment

### **Development Setup**:
1. **Virtual Environment**: Python 3.13 with isolated dependencies
2. **Dependencies**: All packages listed in requirements.txt
3. **Configuration**: Environment variables in .env file
4. **Database**: JSON-based data persistence
5. **File Storage**: Local uploads directory

### **Production Considerations**:
- **WSGI Server**: Use Gunicorn for production deployment
- **Database Migration**: Consider PostgreSQL for production
- **File Storage**: Cloud storage for uploaded files
- **Security**: Enhanced security measures for production
- **Monitoring**: Application monitoring and logging

## 🔄 Change Tracking System

### **Workflow for Updates**:
1. **Modify files** in `Formatted_Project_EDITING/`
2. **Update descriptions** in `Project_Description/` corresponding .md files
3. **Add bullet points** under "Recent Updates" section with date
4. **Update tracker** in `UPDATE_TRACKER.md`
5. **Sync to master** document in `Overall_Project_description/all_edits.md`

### **Update Format**:
```markdown
## 🔄 Recent Updates
- **YYYY-MM-DD**: Brief description of changes
- **YYYY-MM-DD**: Another change description
```

## 📝 Current Project Status

### **Last Major Update**: 2024-10-03
- **Project Reorganization**: Professional directory structure implemented
- **Modular Architecture**: Separated concerns into logical modules
- **Configuration Management**: Centralized settings system
- **Documentation**: Comprehensive project documentation
- **Setup Automation**: Added setup.py for easy installation

### **Active Development Areas**:
- **AI Parsing**: Enhanced transaction extraction accuracy
- **User Interface**: Improved user experience and navigation
- **Bank Integration**: Expanded Plaid API functionality
- **Data Management**: Enhanced transaction and roommate management

## 🎯 Project Goals and Vision

### **Primary Objectives**:
- **Simplify Expense Tracking**: Make roommate expense management effortless
- **AI-Powered Automation**: Reduce manual data entry through AI parsing
- **Real-time Collaboration**: Enable seamless expense sharing
- **Financial Transparency**: Provide clear visibility into spending patterns

### **Technical Goals**:
- **Maintainable Code**: Clean, well-documented, modular architecture
- **Scalable Design**: Support for multiple users and large datasets
- **Security First**: Protect user data and financial information
- **User Experience**: Intuitive, responsive, and accessible interface

This document provides ChatGPT with complete understanding of the Luni Web application, enabling it to assist with development, debugging, feature additions, and maintenance tasks while maintaining awareness of the entire codebase and project architecture.
