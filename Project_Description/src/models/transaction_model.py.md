# transaction_model.py - Data Models and Business Logic

## 📋 File Purpose
- **Data Models**: Defines the structure for transactions and related data
- **Business Logic**: Contains all business rules and calculations
- **Data Persistence**: Handles saving and loading data from JSON files
- **Roommate Management**: Manages roommate relationships and balances

## 🔧 Core Functionality
- **Transaction Management**: CRUD operations for transactions
- **Balance Calculations**: Calculates who owes what to whom
- **Data Validation**: Ensures data integrity and consistency
- **Account Management**: Manages spending categories and sub-accounts

## 📊 Key Classes
- **EnhancedTransactionManager**: Main class for transaction operations
- **Transaction**: Data model for individual transactions
- **Roommate**: Manages roommate information and balances
- **Account**: Handles spending categories and hierarchies

## 🔄 Recent Updates
- **2024-10-03**: Moved from root directory to src/models/ for better organization
- **2024-10-03**: Updated imports to work with new project structure
- **2024-10-03**: No functional changes - maintains all existing functionality

## 🎯 Key Methods
- **add_transaction()**: Adds new transactions to the system
- **get_transactions()**: Retrieves transactions with filtering
- **calculate_balances()**: Computes roommate balances
- **save_data()**: Persists data to JSON file
- **load_data()**: Loads data from JSON file

## 🔧 Data Structure
- **Transactions**: Individual expense records with amounts, dates, categories
- **Roommates**: People involved in expense sharing
- **Accounts**: Spending categories (Food, Transportation, etc.)
- **Balances**: Who owes money to whom

## 🚀 Business Logic
- **Expense Splitting**: Automatically splits expenses between roommates
- **Balance Tracking**: Keeps track of net balances for each person
- **Category Management**: Organizes spending into logical categories
- **Data Validation**: Ensures all data is valid and consistent
