# transactions.json - Data Persistence File

## 📋 File Purpose
- **Data Storage**: Stores all transaction data in JSON format
- **Persistence**: Maintains data between application sessions
- **Backup**: Provides data backup and recovery
- **Portability**: Easy to move data between environments

## 🔧 Core Functionality
- **Transaction Storage**: All transaction records
- **Roommate Data**: Roommate information and balances
- **Account Structure**: Spending categories and hierarchies
- **Settings**: Application configuration and preferences

## 📊 Data Structure
- **Transactions**: Array of transaction objects
- **Roommates**: List of roommate information
- **Accounts**: Spending categories and sub-accounts
- **Settings**: Application preferences and configuration

## 🔄 Recent Updates
- **2024-10-03**: No changes - data structure remains stable
- **2024-10-03**: Maintains all existing transaction data
- **2024-10-03**: Continues to serve as primary data storage

## 🎯 Data Format
```json
{
  "transactions": [...],
  "roommates": [...],
  "accounts": [...],
  "settings": {...}
}
```

## 🔧 Transaction Object
- **id**: Unique transaction identifier
- **amount**: Transaction amount
- **description**: Transaction description
- **date**: Transaction date
- **category**: Spending category
- **roommate**: Associated roommate
- **split_amount**: Amount for this roommate

## 🚀 Features
- **JSON Format**: Human-readable data format
- **Automatic Backup**: Data saved automatically
- **Easy Migration**: Simple to move between systems
- **Data Integrity**: Validates data before saving

## 💡 Benefits
- **Simple Storage**: Easy to understand and modify
- **Portable**: Can be moved between systems
- **Backup Friendly**: Easy to backup and restore
- **Development**: Easy to work with during development
