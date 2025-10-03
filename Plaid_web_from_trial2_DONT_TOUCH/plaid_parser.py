"""
Plaid API Integration for Bank Transaction Retrieval
Handles automatic fetching of bank transactions and conversion to our transaction format
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.configuration import Configuration
from plaid.api_client import ApiClient

# Load environment variables
load_dotenv(override=True)

@dataclass
class PlaidTransaction:
    """Represents a transaction from Plaid API"""
    transaction_id: str
    date: str
    description: str
    amount: float
    type: str  # 'expense' or 'income'
    parent_account: str
    confidence: float = 0.9  # High confidence since it's from bank data
    ai_id: str = None  # Will be set when converted to AITransaction

class PlaidTransactionParser:
    """Handles Plaid API integration for bank transaction retrieval"""
    
    def __init__(self):
        """Initialize Plaid client with API credentials"""
        self.client_id = os.getenv('PLAID_CLIENT_ID')
        self.secret = os.getenv('PLAID_SECRET')
        self.environment = os.getenv('PLAID_ENV', 'sandbox')  # sandbox, development, production
        
        if not self.client_id or not self.secret:
            raise ValueError("Plaid API credentials not found in environment variables")
        
        # Configure Plaid client
        if self.environment == 'sandbox':
            host = plaid.Environment.Sandbox
        elif self.environment == 'development':
            host = plaid.Environment.Development
        elif self.environment == 'production':
            host = plaid.Environment.Production
        else:
            host = plaid.Environment.Sandbox  # Default to sandbox
        
        configuration = Configuration(
            host=host,
            api_key={
                'clientId': self.client_id,
                'secret': self.secret
            }
        )
        
        api_client = ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
        
        print(f"Plaid Parser initialized - Environment: {self.environment}")
        print(f"Plaid Client ID: {self.client_id}")
        print(f"Plaid Environment from .env: {os.getenv('PLAID_ENV')}")
        print(f"Plaid Host: {host}")
    
    def get_recent_transactions(self, access_token: str, days_back: int = 30) -> List[PlaidTransaction]:
        """
        Retrieve recent transactions from Plaid API
        
        Args:
            access_token: Plaid access token for the bank account
            days_back: Number of days to look back for transactions
            
        Returns:
            List of PlaidTransaction objects
        """
        try:
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days_back)
            
            # Create request
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date,
                options=TransactionsGetRequestOptions(
                    count=500,  # Maximum transactions to retrieve
                    offset=0
                )
            )
            
            # Make API call
            response = self.client.transactions_get(request)
            transactions = response['transactions']
            
            print(f"Retrieved {len(transactions)} transactions from Plaid")
            
            # Convert to our format
            plaid_transactions = []
            for transaction in transactions:
                plaid_transaction = self._convert_plaid_transaction(transaction)
                if plaid_transaction:
                    plaid_transactions.append(plaid_transaction)
            
            return plaid_transactions
            
        except Exception as e:
            print(f"Error retrieving transactions from Plaid: {str(e)}")
            return []
    
    def _convert_plaid_transaction(self, transaction: Dict) -> Optional[PlaidTransaction]:
        """
        Convert Plaid transaction to our PlaidTransaction format
        
        Args:
            transaction: Raw transaction data from Plaid API
            
        Returns:
            PlaidTransaction object or None if conversion fails
        """
        try:
            # Extract basic information
            transaction_id = transaction.get('transaction_id', '')
            date = transaction.get('date', '')
            description = transaction.get('name', '')
            amount = transaction.get('amount', 0.0)
            
            # Determine transaction type (Plaid amounts are negative for expenses)
            if amount < 0:
                type_value = 'expense'
                amount = abs(amount)  # Make positive for our system
            else:
                type_value = 'income'
            
            # Generate AI ID for consistency with upload system
            ai_id = f"plaid_{transaction_id}_{int(datetime.now().timestamp())}"
            
            # Try to determine parent account from description
            parent_account = self._classify_transaction(description)
            
            return PlaidTransaction(
                transaction_id=transaction_id,
                date=date,
                description=description,
                amount=amount,
                type=type_value,
                parent_account=parent_account,
                confidence=0.9,  # High confidence from bank data
                ai_id=ai_id
            )
            
        except Exception as e:
            print(f"Error converting Plaid transaction: {str(e)}")
            return None
    
    def _classify_transaction(self, description: str) -> str:
        """
        Classify transaction description into parent account category
        
        Args:
            description: Transaction description from bank
            
        Returns:
            Parent account category
        """
        description_lower = description.lower()
        
        # Food-related keywords
        food_keywords = ['grocery', 'restaurant', 'food', 'coffee', 'dining', 'eat', 'meal', 'cafe', 'bakery', 'market']
        if any(keyword in description_lower for keyword in food_keywords):
            return 'Food'
        
        # Transportation keywords
        transport_keywords = ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'bus', 'transit', 'parking', 'toll', 'car']
        if any(keyword in description_lower for keyword in transport_keywords):
            return 'Transportation'
        
        # Housing keywords
        housing_keywords = ['rent', 'utilities', 'electric', 'water', 'internet', 'cable', 'phone', 'apartment']
        if any(keyword in description_lower for keyword in housing_keywords):
            return 'Housing'
        
        # Education keywords
        education_keywords = ['tuition', 'school', 'university', 'college', 'textbook', 'student', 'education']
        if any(keyword in description_lower for keyword in education_keywords):
            return 'Education'
        
        # Entertainment keywords
        entertainment_keywords = ['movie', 'theater', 'concert', 'game', 'entertainment', 'netflix', 'spotify', 'subscription']
        if any(keyword in description_lower for keyword in entertainment_keywords):
            return 'Entertainment'
        
        # Health keywords
        health_keywords = ['medical', 'doctor', 'pharmacy', 'health', 'insurance', 'hospital', 'clinic']
        if any(keyword in description_lower for keyword in health_keywords):
            return 'Health & Wellness'
        
        # Shopping keywords
        shopping_keywords = ['store', 'shop', 'amazon', 'target', 'walmart', 'clothing', 'shopping']
        if any(keyword in description_lower for keyword in shopping_keywords):
            return 'Shopping'
        
        # Default to Other/Bonus for unclassified transactions
        return 'Other/Bonus'
    
    def get_parsing_statistics(self, transactions: List[PlaidTransaction]) -> Dict:
        """
        Get statistics about parsed transactions
        
        Args:
            transactions: List of PlaidTransaction objects
            
        Returns:
            Dictionary with parsing statistics
        """
        if not transactions:
            return {
                'total_transactions': 0,
                'expense_count': 0,
                'income_count': 0,
                'total_expense': 0.0,
                'total_income': 0.0,
                'account_breakdown': {}
            }
        
        expense_count = sum(1 for t in transactions if t.type == 'expense')
        income_count = sum(1 for t in transactions if t.type == 'income')
        total_expense = sum(t.amount for t in transactions if t.type == 'expense')
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        
        # Account breakdown
        account_breakdown = {}
        for transaction in transactions:
            account = transaction.parent_account
            if account not in account_breakdown:
                account_breakdown[account] = {'count': 0, 'total': 0.0}
            account_breakdown[account]['count'] += 1
            account_breakdown[account]['total'] += transaction.amount
        
        return {
            'total_transactions': len(transactions),
            'expense_count': expense_count,
            'income_count': income_count,
            'total_expense': total_expense,
            'total_income': total_income,
            'account_breakdown': account_breakdown
        }

# Global instance - will be initialized when needed
plaid_parser = None
