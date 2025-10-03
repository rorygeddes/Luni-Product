# Project Overview - Luni Web

## 🎯 Purpose
Luni Web is a Flask-based transaction management system designed for roommate expense tracking and AI-powered receipt parsing. It helps users manage shared expenses, parse receipts automatically, and maintain financial records.

## 🏗️ Architecture

### **Frontend (Templates)**
- **Base Template**: Common layout with navigation
- **Dashboard**: Overview of expenses and roommate balances
- **Upload Interface**: AI-powered receipt parsing
- **Transaction Management**: View, edit, and filter transactions
- **Settings**: Configure roommates, accounts, and payment methods

### **Backend (Python Modules)**

#### **Core Application (`app.py`)**
- Flask web server and routing
- File upload handling
- API endpoints for AJAX requests
- Session management

#### **Data Models (`src/models/transaction_model.py`)**
- Transaction data structure
- Business logic for expense calculations
- Roommate balance tracking
- Data persistence (JSON-based)

#### **AI Integration (`src/parsers/ai_parser.py`)**
- OpenAI Vision API for image parsing
- Receipt text extraction
- Transaction categorization
- Amount and date detection

#### **Bank Integration (`src/parsers/plaid_parser.py`)**
- Plaid API integration
- Bank account connection
- Automatic transaction sync
- Financial data retrieval

### **Configuration (`config/settings.py`)**
- Environment-based configuration
- API key management
- Security settings
- File upload constraints

## 🔄 Data Flow

1. **User uploads receipt/image**
2. **AI Parser extracts transaction data**
3. **Transaction Model validates and stores data**
4. **Dashboard updates with new information**
5. **Roommate balances recalculated**

## 🛠️ Key Technologies

- **Flask**: Web framework
- **OpenAI API**: AI-powered parsing
- **Plaid API**: Bank integration
- **Jinja2**: Template engine
- **Pandas**: Data manipulation
- **Pillow**: Image processing

## 📊 Data Structure

### **Transaction Object**
```python
{
    "id": "unique_id",
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

### **Roommate Balance**
```python
{
    "roommate": "John",
    "total_owed": 150.25,
    "total_owes": 75.50,
    "net_balance": 74.75
}
```

## 🔐 Security Features

- Environment variable configuration
- File upload validation
- Input sanitization
- Secure session management
- API key protection

## 🚀 Deployment Considerations

- **Development**: Debug mode enabled
- **Production**: Use WSGI server (Gunicorn)
- **Database**: Currently JSON-based (consider PostgreSQL for production)
- **File Storage**: Local uploads (consider cloud storage for production)

## 📈 Performance Optimizations

- Lazy loading of transaction data
- Efficient file processing
- Cached AI parsing results
- Optimized database queries

## 🧪 Testing Strategy

- Manual testing of core workflows
- API endpoint validation
- File upload testing
- Error handling verification

## 🔮 Future Enhancements

- Database migration (PostgreSQL)
- Real-time notifications
- Mobile app integration
- Advanced reporting
- Multi-currency support
