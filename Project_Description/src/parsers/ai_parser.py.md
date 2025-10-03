# ai_parser.py - AI-Powered Transaction Parsing

## 📋 File Purpose
- **AI Integration**: Connects to OpenAI Vision API for image analysis
- **Receipt Parsing**: Extracts transaction data from receipt images
- **Text Processing**: Processes extracted text to identify transactions
- **Data Extraction**: Converts images into structured transaction data

## 🔧 Core Functionality
- **Image Analysis**: Uses OpenAI Vision to analyze receipt images
- **Text Extraction**: Extracts text from images and PDFs
- **Transaction Parsing**: Identifies amounts, dates, and descriptions
- **Categorization**: Automatically categorizes transactions

## 📊 Key Classes
- **EnhancedAITransactionParser**: Main parser class
- **AITransaction**: Data model for AI-parsed transactions
- **ImageProcessor**: Handles image preprocessing and format conversion
- **TextAnalyzer**: Processes extracted text for transaction data

## 🔄 Recent Updates
- **2024-10-03**: Moved from root directory to src/parsers/ for better organization
- **2024-10-03**: Updated imports to work with new project structure
- **2024-10-03**: No functional changes - maintains all existing AI capabilities

## 🎯 Key Methods
- **parse_receipt()**: Main method for parsing receipt images
- **extract_text()**: Extracts text from images using OpenAI Vision
- **identify_transactions()**: Finds transaction data in extracted text
- **categorize_transaction()**: Automatically assigns categories
- **validate_data()**: Ensures parsed data is accurate

## 🔧 Supported Formats
- **Images**: JPG, PNG, GIF, BMP, WebP, HEIC
- **Documents**: PDF files
- **Receipts**: Various receipt formats and layouts
- **Bank Statements**: Screenshots and scanned statements

## 🚀 AI Features
- **Smart Parsing**: Uses AI to understand receipt layouts
- **Amount Detection**: Accurately identifies monetary amounts
- **Date Recognition**: Extracts transaction dates
- **Merchant Identification**: Recognizes store names and locations
- **Category Assignment**: Automatically suggests spending categories

## 🔑 API Integration
- **OpenAI Vision API**: For image analysis and text extraction
- **OpenAI Chat API**: For transaction categorization and validation
- **Error Handling**: Robust error handling for API failures
- **Rate Limiting**: Manages API usage and costs
