from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json
import os
import csv
from decimal import Decimal, ROUND_HALF_UP

@dataclass
class Transaction:
    """Enhanced transaction model with better validation and formatting"""
    date: str
    description: str
    amount: float
    account: str
    who_paid: str
    who_will_use: str  # Can be multiple people separated by commas
    method_of_payment: str
    type: str = "expense"  # income or expense
    parent_account: str = "Select"  # parent account category
    id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(self.description) % 10000}"
        
        now = datetime.now().isoformat()
        if self.created_at is None:
            self.created_at = now
        self.updated_at = now
    
    @property
    def formatted_amount(self) -> str:
        """Format amount with proper currency formatting"""
        return f"${self.amount:,.2f}"
    
    @property
    def amount_color(self) -> str:
        """Return color class based on amount"""
        if self.amount < 0:
            return "text-red-600"
        elif self.amount > 0:
            return "text-green-600"
        return "text-gray-600"
    
    @property
    def split_amount(self) -> float:
        """Calculate amount per person when split"""
        users = [user.strip() for user in self.who_will_use.split(',') if user.strip()]
        if not users:
            return 0.0
        return round(self.amount / len(users), 2)

class EnhancedTransactionManager:
    """Enhanced transaction manager with better data handling and validation"""
    
    def __init__(self, data_file: str = "transactions.json"):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self.roommates: List[str] = []
        self.payment_methods: List[str] = []
        self.default_person: str = ""
        
        # Hierarchical account structure: parent -> list of sub-accounts
        self.parent_accounts: Dict[str, List[str]] = {}
        
        # Metadata for better tracking
        self.metadata = {
            'version': '2.0',
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        self.load_data()
    
    def get_default_parent_accounts(self) -> Dict[str, List[str]]:
        """Get comprehensive default parent accounts with sub-accounts"""
        return {
            # Expense Categories
            "Housing": ["Rent", "Utilities", "Internet", "Furniture/essentials"],
            "Food": ["Groceries", "Restaurants", "Dining out", "Coffee", "Snacks"],
            "Transportation": ["Public transit pass", "Gas", "Car insurance & maintenance", "Rideshare", "Bike/scooter"],
            "Education": ["Tuition & fees", "Textbooks", "Supplies"],
            "Personal/Lifestyle": ["Clothing", "Subscription", "Entertainment", "Nights out", "Hobbies", "Sports/gym"],
            "Health & Wellness": ["Health insurance / school plan", "Medication / pharmacy", "Fitness needs", "Haircut"],
            "Savings & Debt": ["Emergency fund", "Credit card payments"],
            
            # Income Categories
            "Employment": ["Part-time jobs", "Side Hustle"],
            "Family Support": ["Allowance", "Gifts", "Family Help"],
            "Loans & Aid": ["Student loans", "Bursaries/Government aid", "Scholarships"],
            "Other/Bonus": ["Investment income", "Refunds / rebates", "Selling items"]
        }
    
    def get_default_payment_methods(self) -> List[str]:
        """Get default payment methods"""
        return ["Debit Card", "Credit Card", "Cash", "Investments", "Bank Transfer", "Mobile Payment"]
    
    def load_data(self):
        """Enhanced data loading with better error handling"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Load transactions with enhanced validation
                    self.transactions = []
                    for t_data in data.get('transactions', []):
                        try:
                            transaction = Transaction(**t_data)
                            self.transactions.append(transaction)
                        except Exception as e:
                            print(f"Warning: Skipping invalid transaction: {e}")
                    
                    # Load other data with fallbacks
                    self.roommates = data.get('roommates', [])
                    self.parent_accounts = data.get('parent_accounts', self.get_default_parent_accounts())
                    self.payment_methods = data.get('payment_methods', self.get_default_payment_methods())
                    self.default_person = data.get('default_person', '')
                    self.metadata = data.get('metadata', self.metadata)
                    
            except Exception as e:
                print(f"Error loading data: {e}")
                self._set_defaults()
        else:
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default values for new installations"""
        self.transactions = []
        self.roommates = []
        self.parent_accounts = self.get_default_parent_accounts()
        self.payment_methods = self.get_default_payment_methods()
        self.default_person = ''
        self.metadata['created_at'] = datetime.now().isoformat()
    
    def save_data(self):
        """Enhanced data saving with metadata tracking"""
        self.metadata['last_updated'] = datetime.now().isoformat()
        
        data = {
            'transactions': [
                {
                    'date': t.date,
                    'description': t.description,
                    'amount': t.amount,
                    'account': t.account,
                    'who_paid': t.who_paid,
                    'who_will_use': t.who_will_use,
                    'method_of_payment': t.method_of_payment,
                    'type': t.type,
                    'parent_account': t.parent_account,
                    'id': t.id,
                    'created_at': t.created_at,
                    'updated_at': t.updated_at
                }
                for t in self.transactions
            ],
            'roommates': self.roommates,
            'parent_accounts': self.parent_accounts,
            'payment_methods': self.payment_methods,
            'default_person': self.default_person,
            'metadata': self.metadata
        }
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
            raise
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add transaction with validation and global defaults"""
        try:
            # Apply global defaults if fields are missing
            if not transaction.who_paid and self.default_person:
                transaction.who_paid = self.default_person
            
            if not transaction.method_of_payment and self.payment_methods:
                transaction.method_of_payment = self.payment_methods[0]
            
            # If who_will_use is empty, use who_paid as fallback
            if not transaction.who_will_use and transaction.who_paid:
                transaction.who_will_use = transaction.who_paid
            
            # Validate transaction
            if not self._validate_transaction(transaction):
                return False
            
            # Check for duplicates
            if self._is_duplicate(transaction):
                return False
            
            self.transactions.append(transaction)
            self.save_data()
            return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False
    
    def _validate_transaction(self, transaction: Transaction) -> bool:
        """Validate transaction data with flexible account validation"""
        if not transaction.date or not transaction.description:
            return False
        
        if not transaction.who_paid or not transaction.who_will_use:
            return False
        
        if not transaction.method_of_payment:
            return False
        
        # Validate account - allow both sub-accounts and parent accounts, empty strings, and "Select" variations
        all_sub_accounts = self.get_all_sub_accounts()
        all_parent_accounts = self.parent_accounts.keys()
        
        # Allow empty accounts, "Select Account", "Select", or valid accounts
        if (transaction.account and 
            transaction.account not in all_sub_accounts and 
            transaction.account not in all_parent_accounts and
            transaction.account != "Select Account" and
            transaction.account != "Select"):
            return False
        
        return True
    
    def _is_duplicate(self, transaction: Transaction) -> bool:
        """Check if transaction is a duplicate"""
        for existing in self.transactions:
            if (existing.date == transaction.date and 
                existing.description.lower() == transaction.description.lower() and
                abs(existing.amount - transaction.amount) < 0.01):
                return True
        return False
    
    def update_transaction(self, transaction_id: str, updates: Dict) -> bool:
        """Update transaction with validation"""
        try:
            transaction = self.get_transaction_by_id(transaction_id)
            if not transaction:
                return False
            
            # Update fields
            for key, value in updates.items():
                if hasattr(transaction, key):
                    setattr(transaction, key, value)
            
            transaction.updated_at = datetime.now().isoformat()
            
            if self._validate_transaction(transaction):
                self.save_data()
                return True
            return False
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete transaction by ID"""
        try:
            self.transactions = [t for t in self.transactions if t.id != transaction_id]
            self.save_data()
            return True
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
    
    def get_all_sub_accounts(self) -> List[str]:
        """Get all sub-accounts from all parent accounts"""
        all_sub_accounts = []
        for sub_accounts in self.parent_accounts.values():
            all_sub_accounts.extend(sub_accounts)
        return all_sub_accounts
    
    def get_sub_accounts_for_parent(self, parent_account: str) -> List[str]:
        """Get sub-accounts for a specific parent"""
        return self.parent_accounts.get(parent_account, [])
    
    def filter_transactions(self, filters: Dict) -> List[Transaction]:
        """Enhanced filtering with better performance"""
        filtered = self.transactions
        
        # Date range filtering
        if 'start_date' in filters and filters['start_date']:
            filtered = [t for t in filtered if t.date >= filters['start_date']]
        
        if 'end_date' in filters and filters['end_date']:
            filtered = [t for t in filtered if t.date <= filters['end_date']]
        
        # Text-based filtering
        if 'description' in filters and filters['description']:
            search_term = filters['description'].lower()
            filtered = [t for t in filtered if search_term in t.description.lower()]
        
        # Exact matching filters
        for field in ['who_paid', 'account', 'method_of_payment', 'type', 'parent_account']:
            if field in filters and filters[field]:
                filtered = [t for t in filtered if getattr(t, field) == filters[field]]
        
        # Enhanced "who_will_use" filtering
        if 'who_will_use' in filters and filters['who_will_use']:
            search_person = filters['who_will_use'].strip()
            filtered = [t for t in filtered if self._person_in_transaction(t, search_person)]
        
        return filtered
    
    def _person_in_transaction(self, transaction: Transaction, person: str) -> bool:
        """Check if person is involved in transaction"""
        # Check who_paid
        if transaction.who_paid == person:
            return True
        
        # Check who_will_use (comma-separated)
        users = [user.strip() for user in transaction.who_will_use.split(',')]
        return person in users
    
    def calculate_balances(self) -> Dict[str, float]:
        """Calculate roommate balances with enhanced logic"""
        balances = {}
        
        # Get all unique people
        all_people = set()
        for transaction in self.transactions:
            all_people.add(transaction.who_paid)
            all_people.update([user.strip() for user in transaction.who_will_use.split(',')])
        
        # Initialize balances
        for person in all_people:
            balances[person] = 0.0
        
        # Calculate balances
        for transaction in self.transactions:
            payer = transaction.who_paid
            users = [user.strip() for user in transaction.who_will_use.split(',') if user.strip()]
            
            if users:
                amount_per_person = transaction.amount / len(users)
                
                # Payer gets credit for the full amount they paid
                balances[payer] += transaction.amount
                
                # Each user owes their share
                for user in users:
                    balances[user] -= amount_per_person
        
        return balances
    
    def get_spending_by_period(self, period: str = 'month') -> Dict:
        """Get spending data by time period"""
        now = datetime.now()
        
        if period == 'week':
            start_date = (now - timedelta(days=7)).strftime('%Y-%m-%d')
        elif period == 'month':
            start_date = now.replace(day=1).strftime('%Y-%m-%d')
        elif period == 'quarter':
            quarter_start = (now.month - 1) // 3 * 3 + 1
            start_date = now.replace(month=quarter_start, day=1).strftime('%Y-%m-%d')
        else:
            start_date = now.strftime('%Y-%m-%d')
        
        end_date = now.strftime('%Y-%m-%d')
        
        period_transactions = self.filter_transactions({
            'start_date': start_date,
            'end_date': end_date,
            'type': 'expense'
        })
        
        spending_by_person = {}
        for transaction in period_transactions:
            person = transaction.who_paid
            spending_by_person[person] = spending_by_person.get(person, 0) + transaction.amount
        
        return {
            'total_spending': sum(t.amount for t in period_transactions),
            'by_person': spending_by_person,
            'transaction_count': len(period_transactions)
        }
    
    def get_parent_account_spending(self, parent_account: str, start_date: str = None, end_date: str = None) -> Dict:
        """Get spending by parent account"""
        filters = {'parent_account': parent_account, 'type': 'expense'}
        if start_date:
            filters['start_date'] = start_date
        if end_date:
            filters['end_date'] = end_date
        
        transactions = self.filter_transactions(filters)
        
        spending_by_sub_account = {}
        for transaction in transactions:
            sub_account = transaction.account
            spending_by_sub_account[sub_account] = spending_by_sub_account.get(sub_account, 0) + transaction.amount
        
        return {
            'total': sum(t.amount for t in transactions),
            'by_sub_account': spending_by_sub_account,
            'transaction_count': len(transactions)
        }
    
    def parse_csv_transactions(self, csv_file_path: str) -> Tuple[List[Dict], List[str]]:
        """Enhanced CSV parsing with better validation"""
        transactions = []
        errors = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Validate required fields
                        required_fields = ['Date', 'Description', 'Amount', 'Account', 'Who Paid', 'Who Will Use', 'Method of Payment']
                        missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                        
                        if missing_fields:
                            errors.append(f"Row {row_num}: Missing required fields: {', '.join(missing_fields)}")
                            continue
                        
                        # Validate data against system
                        if row['Who Paid'] not in self.roommates:
                            errors.append(f"Row {row_num}: 'Who Paid' ({row['Who Paid']}) not found in roommates list")
                            continue
                        
                        if row['Method of Payment'] not in self.payment_methods:
                            errors.append(f"Row {row_num}: 'Method of Payment' ({row['Method of Payment']}) not found in payment methods list")
                            continue
                        
                        all_sub_accounts = self.get_all_sub_accounts()
                        if row['Account'] not in all_sub_accounts:
                            errors.append(f"Row {row_num}: 'Account' ({row['Account']}) not found in accounts list")
                            continue
                        
                        # Parse amount
                        try:
                            amount = float(row['Amount'].replace('$', '').replace(',', ''))
                        except ValueError:
                            errors.append(f"Row {row_num}: Invalid amount format: {row['Amount']}")
                            continue
                        
                        transactions.append({
                            'date': row['Date'],
                            'description': row['Description'],
                            'amount': amount,
                            'account': row['Account'],
                            'who_paid': row['Who Paid'],
                            'who_will_use': row['Who Will Use'],
                            'method_of_payment': row['Method of Payment'],
                            'type': row.get('Type', 'expense'),
                            'parent_account': row.get('Parent Account', 'Select')
                        })
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: Error processing row: {str(e)}")
                        continue
                        
        except Exception as e:
            errors.append(f"Error reading CSV file: {str(e)}")
        
        return transactions, errors
    
    # Account management methods
    def add_parent_account(self, parent_account: str) -> bool:
        """Add a new parent account"""
        if parent_account not in self.parent_accounts:
            self.parent_accounts[parent_account] = []
            self.save_data()
            return True
        return False
    
    def remove_parent_account(self, parent_account: str) -> bool:
        """Remove a parent account and its sub-accounts"""
        if parent_account in self.parent_accounts:
            del self.parent_accounts[parent_account]
            self.save_data()
            return True
        return False
    
    def add_sub_account(self, parent_account: str, sub_account: str) -> bool:
        """Add a sub-account to a parent account"""
        if parent_account in self.parent_accounts:
            if sub_account not in self.parent_accounts[parent_account]:
                self.parent_accounts[parent_account].append(sub_account)
                self.save_data()
                return True
        return False
    
    def remove_sub_account(self, parent_account: str, sub_account: str) -> bool:
        """Remove a sub-account from a parent account"""
        if parent_account in self.parent_accounts:
            if sub_account in self.parent_accounts[parent_account]:
                self.parent_accounts[parent_account].remove(sub_account)
                self.save_data()
                return True
        return False
    
    # Roommate and payment method management
    def add_roommate(self, roommate: str) -> bool:
        """Add a new roommate"""
        if roommate not in self.roommates:
            self.roommates.append(roommate)
            self.save_data()
            return True
        return False
    
    def remove_roommate(self, roommate: str) -> bool:
        """Remove a roommate"""
        if roommate in self.roommates:
            self.roommates.remove(roommate)
            self.save_data()
            return True
        return False
    
    def add_payment_method(self, method: str) -> bool:
        """Add a new payment method"""
        if method not in self.payment_methods:
            self.payment_methods.append(method)
            self.save_data()
            return True
        return False
    
    def remove_payment_method(self, method: str) -> bool:
        """Remove a payment method"""
        if method in self.payment_methods:
            self.payment_methods.remove(method)
            self.save_data()
            return True
        return False
    
    def set_default_person(self, person: str) -> bool:
        """Set the default person"""
        self.default_person = person
        self.save_data()
        return True
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about the system"""
        total_transactions = len(self.transactions)
        total_roommates = len(self.roommates)
        total_accounts = len(self.get_all_sub_accounts())
        
        balances = self.calculate_balances()
        positive_balances = sum(1 for b in balances.values() if b > 0)
        negative_balances = sum(1 for b in balances.values() if b < 0)
        
        return {
            'total_transactions': total_transactions,
            'total_roommates': total_roommates,
            'total_accounts': total_accounts,
            'total_people_with_positive_balances': positive_balances,
            'total_people_with_negative_balances': negative_balances,
            'data_file_size': os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0,
            'last_updated': self.metadata.get('last_updated', 'Unknown')
        }

    def calculate_spending_overview(self, transactions=None):
        """Calculate comprehensive spending overview for given transactions"""
        if transactions is None:
            transactions = self.transactions
        
        # Basic calculations
        total_spent = sum(t.amount for t in transactions if t.type == 'expense')
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_transactions = len(transactions)
        
        # Calculate oweings (simplified - this could be more complex)
        total_oweings = 0  # For now, we'll keep this simple
        
        # Net amount = income - spent + oweings
        net_amount = total_income - total_spent + total_oweings
        
        return {
            'total_spent': total_spent,
            'total_income': total_income,
            'total_oweings': total_oweings,
            'net_amount': net_amount,
            'transaction_count': total_transactions
        }

    def calculate_roommate_breakdown(self, transactions=None):
        """Calculate roommate spending breakdown excluding default person"""
        if transactions is None:
            transactions = self.transactions
        
        # Get non-default roommates
        non_default_roommates = [r for r in self.roommates if r != self.default_person]
        
        # Initialize roommate data
        roommate_data = {}
        for roommate in non_default_roommates:
            roommate_data[roommate] = {
                'spent': 0,
                'owes': 0,
                'owed': 0,
                'balance': 0
            }
        
        # Process transactions
        for transaction in transactions:
            if transaction.type == 'expense':
                who_paid = transaction.who_paid
                who_will_use = transaction.who_will_use.split(',') if transaction.who_will_use else []
                who_will_use = [user.strip() for user in who_will_use]
                
                # Track what each roommate spent
                if who_paid in roommate_data:
                    roommate_data[who_paid]['spent'] += transaction.amount
                
                # Calculate owes/owed relationships
                if who_will_use:
                    amount_per_user = transaction.amount / len(who_will_use)
                    
                    for user in who_will_use:
                        if user in roommate_data:
                            if user == who_paid:
                                # This person paid, so others owe them
                                roommate_data[user]['owed'] += transaction.amount - amount_per_user
                            else:
                                # This person owes the payer
                                roommate_data[user]['owes'] += amount_per_user
                
                # Also handle case where default person paid for non-default roommates
                elif who_paid == self.default_person and non_default_roommates:
                    # Default person paid, so all non-default roommates owe them
                    amount_per_roommate = transaction.amount / len(non_default_roommates)
                    for roommate in non_default_roommates:
                        roommate_data[roommate]['owes'] += amount_per_roommate
        
        # Calculate final balances
        for roommate in roommate_data:
            data = roommate_data[roommate]
            data['balance'] = data['owed'] - data['owes']
        
        return roommate_data

    def update_transaction(self, transaction_id: str, **updates) -> bool:
        """Update a transaction with new values"""
        try:
            for transaction in self.transactions:
                if transaction.id == transaction_id:
                    # Update fields that are provided
                    for field, value in updates.items():
                        if hasattr(transaction, field):
                            setattr(transaction, field, value)
                    
                    # Re-validate the transaction
                    if self._validate_transaction(transaction):
                        self.save_data()
                        return True
                    else:
                        return False
            
            return False  # Transaction not found
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
