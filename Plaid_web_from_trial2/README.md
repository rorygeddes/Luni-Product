# Luni Web - Trial 2 (Enhanced Version)

An enhanced transaction tracker with AI-powered receipt parsing and roommate expense management.

## Features

### Core Functionality
- **AI Receipt Parsing**: Upload receipts, bank statements, and screenshots for automatic transaction extraction
- **Roommate Expense Tracking**: Split expenses and track who owes what
- **Hierarchical Account Management**: Organize spending into parent categories and sub-accounts
- **Real-time Dashboard**: View spending summaries and roommate balances
- **CSV Batch Import**: Upload multiple transactions at once

### Enhanced Features (Trial 2)
- **Improved UI/UX**: Modern, responsive design with better navigation
- **Advanced AI Integration**: Enhanced transaction parsing with better accuracy
- **Real-time Updates**: Live dashboard updates as transactions are added/modified
- **Better Data Management**: Improved data persistence and validation
- **Enhanced Filtering**: More powerful filtering and search capabilities

## Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Copy your OpenAI API key to the `.env` file
   - Replace `your-api-key-here` with your actual API key

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   - Open http://127.0.0.1:3001 in your browser

## Navigation Order
1. **Dashboard** - Overview of spending and roommate balances
2. **Upload** - AI parsing and CSV import functionality
3. **All Transactions** - View, filter, and edit all transactions
4. **Information** - Manage roommates, accounts, and payment methods
5. **Input Transaction** - Manual transaction entry

## File Structure
```
trial2/
├── app.py                 # Main Flask application
├── transaction_model.py   # Data models and business logic
├── ai_parser.py          # AI transaction parsing
├── templates/            # HTML templates
├── static/              # CSS and JavaScript files
├── uploads/             # File upload directory
└── transactions.json    # Data persistence
```

## API Integration
- **OpenAI Vision API**: For image-to-text extraction
- **OpenAI Chat Completions**: For transaction classification and categorization
- **Plaid API**: For automatic bank transaction retrieval

## Environment Variables
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your-openai-api-key-here
PLAID_CLIENT_ID=your-plaid-client-id-here
PLAID_SECRET=your-plaid-secret-here
PLAID_ENV=sandbox
```

## Default Data
The system comes with pre-configured:
- **Account Categories**: Housing, Food, Transportation, Education, etc.
- **Payment Methods**: Debit Card, Credit Card, Cash, Investments
- **Sample Data**: Ready-to-use account structure for student spending
