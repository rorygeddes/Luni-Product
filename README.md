# Luni Web - Transaction Management System

A Flask-based web application for AI-powered transaction parsing, roommate expense tracking, and financial data management.

## 🏗️ Project Structure

```
Formatted_Project_EDITING/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── transactions.json         # Data persistence file
├── uploads/                  # File upload directory
├── templates/                # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── all_transactions.html
│   ├── plaid_transactions.html
│   ├── input_transaction.html
│   └── information.html
├── src/                      # Source code modules
│   ├── models/               # Data models
│   │   └── transaction_model.py
│   └── parsers/              # Data parsers
│       ├── ai_parser.py
│       └── plaid_parser.py
├── config/                   # Configuration
│   └── settings.py
├── docs/                     # Documentation
│   ├── ai_fixes.md
│   ├── all_transactions.md
│   └── upload_screen.md
└── venv/                     # Virtual environment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Local Development

1. **Clone and navigate to the project:**
   ```bash
   cd Formatted_Project_EDITING
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   - Open http://localhost:3000 in your browser

### 🚀 Vercel Deployment

For production deployment to Vercel:

1. **Follow the Vercel deployment guide**: See `VERCEL_DEPLOYMENT.md`
2. **Connect your GitHub repository** to Vercel
3. **Set environment variables** in Vercel dashboard
4. **Deploy automatically** on every GitHub push

**Quick Vercel Setup:**
- Import repository to Vercel
- Set root directory to `Formatted_Project_EDITING`
- Add environment variables (OPENAI_API_KEY, etc.)
- Deploy!

## 🔧 Core Components

### 1. **Flask Application (`app.py`)**
- Main web server and routing
- Handles file uploads and API endpoints
- Manages session data and user interactions

### 2. **Transaction Model (`src/models/transaction_model.py`)**
- Core business logic for transaction management
- Data validation and persistence
- Roommate expense calculations

### 3. **AI Parser (`src/parsers/ai_parser.py`)**
- OpenAI Vision API integration
- Receipt and document parsing
- Transaction extraction and categorization

### 4. **Plaid Parser (`src/parsers/plaid_parser.py`)**
- Bank account integration
- Automatic transaction retrieval
- Financial data synchronization

### 5. **Configuration (`config/settings.py`)**
- Environment-based configuration
- API key management
- Security settings

## 📊 Key Features

### AI-Powered Transaction Parsing
- Upload receipts, bank statements, screenshots
- Automatic transaction extraction using OpenAI Vision
- Smart categorization and amount detection

### Roommate Expense Management
- Split expenses between roommates
- Track who owes what
- Balance calculations and notifications

### Financial Data Management
- Hierarchical account structure
- Multiple payment methods
- Transaction filtering and search

### Bank Integration (Optional)
- Plaid API integration
- Automatic bank transaction sync
- Secure financial data access

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirects to dashboard |
| `/dashboard` | GET | Main dashboard view |
| `/upload` | GET/POST | File upload interface |
| `/all_transactions` | GET | Transaction list view |
| `/plaid_transactions` | GET | Plaid integration |
| `/input_transaction` | GET/POST | Manual transaction entry |
| `/information` | GET | Settings and configuration |

## 🛠️ Development

### Code Organization
- **Models**: Business logic and data structures
- **Parsers**: External API integrations
- **Templates**: HTML views with Jinja2 templating
- **Configuration**: Environment-based settings

### Adding New Features
1. Create new modules in appropriate `src/` subdirectories
2. Update `app.py` with new routes
3. Add corresponding templates
4. Update configuration as needed

### Testing
```bash
# Run the application in debug mode
python app.py
```

## 🔐 Security Considerations

- API keys stored in environment variables
- File upload validation and sanitization
- Secure session management
- Input validation and error handling

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for AI parsing |
| `PLAID_CLIENT_ID` | No | Plaid client ID for bank integration |
| `PLAID_SECRET` | No | Plaid secret for bank integration |
| `SECRET_KEY` | No | Flask secret key (auto-generated) |

## 🐛 Troubleshooting

### Common Issues
1. **API Key Not Loading**: Check `.env` file exists and contains valid key
2. **Port Already in Use**: Change port in `app.py` or kill existing process
3. **Import Errors**: Ensure virtual environment is activated and dependencies installed

### Debug Mode
The application runs in debug mode by default, providing:
- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger

## 📚 Documentation

- `docs/ai_fixes.md` - AI parsing improvements
- `docs/all_transactions.md` - Transaction management features
- `docs/upload_screen.md` - Upload interface documentation

## 🤝 Contributing

1. Follow the established project structure
2. Add proper error handling
3. Update documentation for new features
4. Test thoroughly before submitting changes

## 📄 License

This project is for educational and personal use.