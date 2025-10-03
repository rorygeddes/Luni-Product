from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, flash
from transaction_model import EnhancedTransactionManager, Transaction
from ai_parser import EnhancedAITransactionParser, AITransaction
try:
    from plaid_parser import PlaidTransactionParser, PlaidTransaction
    PLAID_AVAILABLE = True
except ImportError:
    PLAID_AVAILABLE = False
    print("Plaid parser not available - install plaid-python and set credentials")
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import tempfile
from dotenv import load_dotenv
import json

# Load environment variables first
load_dotenv(override=True)

# Debug: Check if API key is loaded correctly
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key loaded in Flask app: {api_key[:20] + '...' if api_key and len(api_key) > 20 else api_key}")

app = Flask(__name__)
app.secret_key = 'luni-web-enhanced-secret-key-2024'  # For flash messages

# Initialize managers
transaction_manager = EnhancedTransactionManager()
ai_parser = EnhancedAITransactionParser()

# Global storage for AI transactions and extracted texts
ai_transactions = []
extracted_texts = []

# Global storage for Plaid transactions
plaid_transactions_list = []
plaid_parser = None

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
AI_ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'heic', 'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_ai_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in AI_ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Enhanced dashboard with better statistics and real-time updates"""
    try:
        # Get comprehensive statistics
        stats = transaction_manager.get_statistics()
        
        # Get spending data for different periods
        week_spending = transaction_manager.get_spending_by_period('week')
        month_spending = transaction_manager.get_spending_by_period('month')
        quarter_spending = transaction_manager.get_spending_by_period('quarter')
        
        # Get roommate balances
        balances = transaction_manager.calculate_balances()
        
        # Get parent account spending
        parent_account_spending = {}
        for parent_account in transaction_manager.parent_accounts.keys():
            parent_account_spending[parent_account] = transaction_manager.get_parent_account_spending(parent_account)
        
        return render_template('dashboard.html',
                             stats=stats,
                             week_spending=week_spending,
                             month_spending=month_spending,
                             quarter_spending=quarter_spending,
                             balances=balances,
                             parent_account_spending=parent_account_spending,
                             parent_accounts=transaction_manager.parent_accounts)
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", 'error')
        return render_template('dashboard.html',
                             stats={},
                             week_spending={},
                             month_spending={},
                             quarter_spending={},
                             balances={},
                             parent_account_spending={},
                             parent_accounts={})

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Enhanced upload page with better AI integration"""
    global ai_transactions, extracted_texts
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'upload_ai_files':
            if 'ai_file' not in request.files:
                flash('No file selected', 'error')
                return redirect(url_for('upload'))
            
            file = request.files['ai_file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('upload'))
            
            if file and allowed_ai_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                try:
                    # Parse image for transactions
                    transactions, extracted_text, success = ai_parser.parse_image_for_transactions(filepath)
                    
                    if success and transactions:
                        ai_transactions.extend(transactions)
                        extracted_texts.append({
                            'filename': filename,
                            'text': extracted_text,
                            'timestamp': datetime.now().isoformat()
                        })
                        flash(f'Successfully parsed {len(transactions)} transactions from {filename}', 'success')
                    else:
                        flash(f'No transactions found in {filename}. Check the extracted text below.', 'warning')
                        extracted_texts.append({
                            'filename': filename,
                            'text': extracted_text,
                            'timestamp': datetime.now().isoformat()
                        })
                
                except Exception as e:
                    flash(f'Error parsing {filename}: {str(e)}', 'error')
                
                # Clean up uploaded file
                try:
                    os.remove(filepath)
                except:
                    pass
            
            return redirect(url_for('upload'))
        
        elif action == 'upload_csv':
            if 'csv_file' not in request.files:
                flash('No CSV file selected', 'error')
                return redirect(url_for('upload'))
            
            file = request.files['csv_file']
            if file.filename == '':
                flash('No CSV file selected', 'error')
                return redirect(url_for('upload'))
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                try:
                    transactions, errors = transaction_manager.parse_csv_transactions(filepath)
                    
                    if errors:
                        for error in errors:
                            flash(error, 'error')
                    
                    if transactions:
                        # Add transactions to AI transactions for review
                        for t_data in transactions:
                            ai_transaction = AITransaction(
                                date=t_data['date'],
                                description=t_data['description'],
                                amount=t_data['amount'],
                                type=t_data['type'],
                                parent_account=t_data['parent_account']
                            )
                            ai_transactions.append(ai_transaction)
                        
                        flash(f'Successfully loaded {len(transactions)} transactions from CSV', 'success')
                    else:
                        flash('No valid transactions found in CSV file', 'warning')
                
                except Exception as e:
                    flash(f'Error processing CSV: {str(e)}', 'error')
                
                # Clean up uploaded file
                try:
                    os.remove(filepath)
                except:
                    pass
            
            return redirect(url_for('upload'))
        
        elif action == 'add_to_transactions':
            global_who_paid = request.form.get('global_who_paid')
            global_payment_method = request.form.get('global_payment_method')
            
            # Use defaults if not provided
            if not global_who_paid:
                global_who_paid = transaction_manager.default_person
            if not global_payment_method and transaction_manager.payment_methods:
                global_payment_method = transaction_manager.payment_methods[0]
            
            # Get all AI transactions from the form
            transactions_to_add = []
            transactions_to_remove = []
            
            for ai_transaction in ai_transactions:
                # Get form values - capture updated values from form, not original AI values
                date = request.form.get(f'date_{ai_transaction.ai_id}', ai_transaction.date)
                description = request.form.get(f'description_{ai_transaction.ai_id}', ai_transaction.description)
                amount = request.form.get(f'amount_{ai_transaction.ai_id}', ai_transaction.amount)
                type_value = request.form.get(f'type_{ai_transaction.ai_id}', ai_transaction.type)
                account = request.form.get(f'account_{ai_transaction.ai_id}', '')
                who_will_use = request.form.get(f'who_will_use_{ai_transaction.ai_id}', '')
                parent_account = request.form.get(f'parent_account_{ai_transaction.ai_id}', ai_transaction.parent_account)
                
                # Convert amount to float if it's a string
                try:
                    amount = float(amount) if amount else ai_transaction.amount
                except (ValueError, TypeError):
                    amount = ai_transaction.amount
                
                # Debug logging
                print(f"Transaction {ai_transaction.ai_id} form data:")
                print(f"  Date: {date} (original: {ai_transaction.date})")
                print(f"  Description: {description} (original: {ai_transaction.description})")
                print(f"  Amount: {amount} (original: {ai_transaction.amount})")
                print(f"  Type: {type_value} (original: {ai_transaction.type})")
                print(f"  Account: {account}")
                print(f"  Who will use: {who_will_use}")
                print(f"  Who paid: {global_who_paid}")
                print(f"  Payment method: {global_payment_method}")
                print(f"  Parent account: {parent_account}")
                
                # Create Transaction object with updated form values
                transaction = Transaction(
                    date=date,
                    description=description,
                    amount=amount,
                    account=account,
                    who_paid=global_who_paid,
                    who_will_use=who_will_use,
                    method_of_payment=global_payment_method,
                    type=type_value,
                    parent_account=parent_account
                )
                
                # Add transaction (validation and defaults handled in add_transaction method)
                if transaction_manager.add_transaction(transaction):
                    transactions_to_add.append(transaction)
                    transactions_to_remove.append(ai_transaction)
                else:
                    # Log the failure but continue processing other transactions
                    print(f"Failed to add transaction: {transaction.description}")
                    flash(f'Failed to add transaction: {transaction.description}', 'error')
            
            # Remove successfully added transactions from AI list
            for transaction in transactions_to_remove:
                ai_transactions.remove(transaction)
            
            # Report results
            total_attempted = len(ai_transactions) + len(transactions_to_add)
            successful = len(transactions_to_add)
            failed = total_attempted - successful
            
            if successful > 0:
                flash(f'Successfully added {successful} transactions', 'success')
            if failed > 0:
                flash(f'{failed} transactions failed to add. Please check the errors above.', 'error')
            if successful == 0 and failed == 0:
                flash('No transactions to process', 'warning')
            
            return redirect(url_for('upload'))
        
        elif action == 'clear_ai_transactions':
            ai_transactions.clear()
            extracted_texts.clear()
            flash('Cleared all AI transactions', 'info')
            return redirect(url_for('upload'))
    
    # Get parsing statistics
    parsing_stats = ai_parser.get_parsing_statistics(ai_transactions) if ai_transactions else {}
    
    # Sort transactions by confidence level (lowest to highest)
    sorted_ai_transactions = sorted(ai_transactions, key=lambda x: x.confidence)
    
    return render_template('upload.html',
                         ai_transactions=sorted_ai_transactions,
                         extracted_texts=extracted_texts,
                         parsing_stats=parsing_stats,
                         roommates=transaction_manager.roommates,
                         payment_methods=transaction_manager.payment_methods,
                         parent_accounts=transaction_manager.parent_accounts,
                         all_sub_accounts=transaction_manager.get_all_sub_accounts(),
                         default_person=transaction_manager.default_person)

@app.route('/plaid_link_token', methods=['POST'])
def plaid_link_token():
    """Create a Plaid Link token for the user"""
    try:
        if not PLAID_AVAILABLE:
            return jsonify({'error': 'Plaid not available'}), 500
        
        # Initialize parser if needed
        global plaid_parser
        if plaid_parser is None:
            plaid_parser = PlaidTransactionParser()
        
        # Get user data from request
        data = request.get_json()
        user_id = data.get('user_id', 'luni_user')
        
        # Create link token
        link_token_response = plaid_parser.client.link_token_create({
            'user': {
                'client_user_id': user_id,
            },
            'client_name': 'Luni Web',
            'products': ['transactions'],
            'country_codes': ['CA', 'US'],  # Prioritize Canada first
            'language': 'en',
        })
        
        return jsonify({
            'link_token': link_token_response['link_token'],
            'expiration': link_token_response['expiration']
        })
        
    except Exception as e:
        print(f"Error creating link token: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/plaid_transactions', methods=['GET', 'POST'])
def plaid_transactions():
    """Plaid Transactions page for automatic bank transaction retrieval"""
    global plaid_transactions_list, plaid_parser
    
    # Check if Plaid is available
    if not PLAID_AVAILABLE:
        flash('Plaid integration is not available. Please install plaid-python and set up API credentials.', 'error')
        return render_template('plaid_transactions.html',
                             plaid_transactions=[],
                             roommates=transaction_manager.roommates,
                             payment_methods=transaction_manager.payment_methods,
                             parent_accounts=transaction_manager.parent_accounts,
                             default_person=transaction_manager.default_person,
                             all_sub_accounts=transaction_manager.get_all_sub_accounts(),
                             parsing_stats={})
    
    # Initialize Plaid parser if not already done
    if plaid_parser is None:
        try:
            plaid_parser = PlaidTransactionParser()
        except Exception as e:
            flash(f'Error initializing Plaid parser: {str(e)}', 'error')
            plaid_parser = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'exchange_token':
            # Handle Plaid Link token exchange
            public_token = request.form.get('public_token')
            days_back = int(request.form.get('days_back', 30))
            
            try:
                # Exchange public token for access token
                exchange_response = plaid_parser.client.item_public_token_exchange({
                    'public_token': public_token
                })
                access_token = exchange_response['access_token']
                
                # Fetch transactions using the access token
                transactions = plaid_parser.get_recent_transactions(access_token, days_back)
                
                if transactions:
                    plaid_transactions_list.extend(transactions)
                    flash(f'Successfully fetched {len(transactions)} transactions from your bank account!', 'success')
                else:
                    flash('No new transactions found in your bank account.', 'info')
                
                return jsonify({'success': True, 'transactions_count': len(transactions)})
                
            except Exception as e:
                print(f"Error exchanging token: {e}")
                return jsonify({'success': False, 'error': str(e)})
        
        elif action == 'fetch_transactions':
            # Get access token from form (in real implementation, this would be stored securely)
            access_token = request.form.get('access_token', '').strip()
            days_back = int(request.form.get('days_back', 30))
            
            if not access_token:
                flash('Please provide a valid access token', 'error')
                return redirect(url_for('plaid_transactions'))
            
            if plaid_parser:
                try:
                    # Fetch transactions from Plaid
                    new_transactions = plaid_parser.get_recent_transactions(access_token, days_back)
                    
                    if new_transactions:
                        # Add to global plaid_transactions list
                        plaid_transactions_list.extend(new_transactions)
                        flash(f'Successfully retrieved {len(new_transactions)} transactions from Plaid', 'success')
                    else:
                        flash('No new transactions found', 'info')
                        
                except Exception as e:
                    flash(f'Error fetching transactions from Plaid: {str(e)}', 'error')
            else:
                flash('Plaid parser not initialized', 'error')
            
            return redirect(url_for('plaid_transactions'))
        
        elif action == 'add_to_transactions':
            global_who_paid = request.form.get('global_who_paid')
            global_payment_method = request.form.get('global_payment_method')
            
            # Use defaults if not provided
            if not global_who_paid:
                global_who_paid = transaction_manager.default_person
            if not global_payment_method and transaction_manager.payment_methods:
                global_payment_method = transaction_manager.payment_methods[0]
            
            # Get all Plaid transactions from the form
            transactions_to_add = []
            transactions_to_remove = []
            
            for plaid_transaction in plaid_transactions_list:
                # Get form values - capture updated values from form, not original Plaid values
                date = request.form.get(f'date_{plaid_transaction.ai_id}', plaid_transaction.date)
                description = request.form.get(f'description_{plaid_transaction.ai_id}', plaid_transaction.description)
                amount = request.form.get(f'amount_{plaid_transaction.ai_id}', plaid_transaction.amount)
                type_value = request.form.get(f'type_{plaid_transaction.ai_id}', plaid_transaction.type)
                account = request.form.get(f'account_{plaid_transaction.ai_id}', '')
                who_will_use = request.form.get(f'who_will_use_{plaid_transaction.ai_id}', '')
                parent_account = request.form.get(f'parent_account_{plaid_transaction.ai_id}', plaid_transaction.parent_account)
                
                # Convert amount to float if it's a string
                try:
                    amount = float(amount) if amount else plaid_transaction.amount
                except (ValueError, TypeError):
                    amount = plaid_transaction.amount
                
                # Create Transaction object with updated form values
                transaction = Transaction(
                    date=date,
                    description=description,
                    amount=amount,
                    account=account,
                    who_paid=global_who_paid,
                    who_will_use=who_will_use,
                    method_of_payment=global_payment_method,
                    type=type_value,
                    parent_account=parent_account
                )
                
                # Add transaction (validation and defaults handled in add_transaction method)
                if transaction_manager.add_transaction(transaction):
                    transactions_to_add.append(transaction)
                    transactions_to_remove.append(plaid_transaction)
                else:
                    # Log the failure but continue processing other transactions
                    print(f"Failed to add Plaid transaction: {transaction.description}")
                    flash(f'Failed to add transaction: {transaction.description}', 'error')
            
            # Remove successfully added transactions from Plaid list
            for transaction in transactions_to_remove:
                plaid_transactions_list.remove(transaction)
            
            # Report results
            total_attempted = len(plaid_transactions_list) + len(transactions_to_add)
            successful = len(transactions_to_add)
            failed = total_attempted - successful
            
            if successful > 0:
                flash(f'Successfully added {successful} transactions', 'success')
            if failed > 0:
                flash(f'{failed} transactions failed to add. Please check the errors above.', 'error')
            if successful == 0 and failed == 0:
                flash('No transactions to process', 'warning')
            
            return redirect(url_for('plaid_transactions'))
        
        elif action == 'clear_plaid_transactions':
            plaid_transactions_list.clear()
            flash('Cleared all Plaid transactions', 'info')
            return redirect(url_for('plaid_transactions'))
    
    # Get parsing statistics
    parsing_stats = plaid_parser.get_parsing_statistics(plaid_transactions_list) if plaid_parser and plaid_transactions_list else {}
    
    return render_template('plaid_transactions.html',
                         plaid_transactions=plaid_transactions_list,
                         roommates=transaction_manager.roommates,
                         payment_methods=transaction_manager.payment_methods,
                         parent_accounts=transaction_manager.parent_accounts,
                         default_person=transaction_manager.default_person,
                         all_sub_accounts=transaction_manager.get_all_sub_accounts(),
                         parsing_stats=parsing_stats)

@app.route('/all_transactions')
def all_transactions():
    """Enhanced all transactions page with better filtering"""
    # Get filter parameters
    filters = {}
    for field in ['date', 'description', 'who_paid', 'account', 'method_of_payment', 'type', 'parent_account', 'who_will_use']:
        value = request.args.get(field, '').strip()
        if value:
            filters[field] = value
    
    # Date range filtering - check if period is specified
    period = request.args.get('period', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    
    # If period is specified, calculate dates automatically
    if period and not start_date and not end_date:
        from datetime import datetime, timedelta
        now = datetime.now()
        
        if period == 'week':
            start_date = (now - timedelta(days=now.weekday())).strftime('%Y-%m-%d')
            end_date = (now - timedelta(days=now.weekday()) + timedelta(days=6)).strftime('%Y-%m-%d')
        elif period == 'month':
            start_date = now.replace(day=1).strftime('%Y-%m-%d')
            if now.month == 12:
                end_date = now.replace(year=now.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = now.replace(month=now.month + 1, day=1) - timedelta(days=1)
            end_date = end_date.strftime('%Y-%m-%d')
        elif period == 'quarter':
            start_date = (now - timedelta(days=90)).strftime('%Y-%m-%d')
            end_date = now.strftime('%Y-%m-%d')
        elif period == 'custom':
            # Keep existing dates if custom is selected
            pass
    
    if start_date:
        filters['start_date'] = start_date
    if end_date:
        filters['end_date'] = end_date
    
    # Get filtered transactions
    filtered_transactions = transaction_manager.filter_transactions(filters)
    
    # Sort by date (newest first)
    filtered_transactions.sort(key=lambda x: x.date, reverse=True)
    
    # Calculate spending overview and roommate breakdown server-side
    spending_overview = transaction_manager.calculate_spending_overview(filtered_transactions)
    roommate_breakdown = transaction_manager.calculate_roommate_breakdown(filtered_transactions)
    
    return render_template('all_transactions.html',
                         transactions=filtered_transactions,
                         filters=filters,
                         selected_period=period or 'month',  # Default to month if no period specified
                         roommates=transaction_manager.roommates,
                         payment_methods=transaction_manager.payment_methods,
                         parent_accounts=transaction_manager.parent_accounts,
                         default_person=transaction_manager.default_person,
                         all_sub_accounts=transaction_manager.get_all_sub_accounts(),
                         spending_overview=spending_overview,
                         roommate_breakdown=roommate_breakdown)

@app.route('/information', methods=['GET', 'POST'])
def information():
    """Enhanced information management page"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'set_default_person':
            default_person = request.form.get('default_person_name', '').strip()
            if default_person:
                transaction_manager.set_default_person(default_person)
                flash(f'Default person set to {default_person}', 'success')
            else:
                flash('Default person name cannot be empty', 'error')
        
        elif action == 'add_roommate':
            roommate = request.form.get('roommate_name', '').strip()
            if roommate:
                if transaction_manager.add_roommate(roommate):
                    flash(f'Added roommate: {roommate}', 'success')
                else:
                    flash(f'Roommate {roommate} already exists', 'warning')
            else:
                flash('Roommate name cannot be empty', 'error')
        
        elif action == 'remove_roommate':
            roommate = request.form.get('roommate_to_remove', '').strip()
            if roommate:
                if transaction_manager.remove_roommate(roommate):
                    flash(f'Removed roommate: {roommate}', 'success')
                else:
                    flash(f'Roommate {roommate} not found', 'error')
        
        elif action == 'add_payment_method':
            method = request.form.get('payment_method_name', '').strip()
            if method:
                if transaction_manager.add_payment_method(method):
                    flash(f'Added payment method: {method}', 'success')
                else:
                    flash(f'Payment method {method} already exists', 'warning')
            else:
                flash('Payment method name cannot be empty', 'error')
        
        elif action == 'remove_payment_method':
            method = request.form.get('payment_method_to_remove', '').strip()
            if method:
                if transaction_manager.remove_payment_method(method):
                    flash(f'Removed payment method: {method}', 'success')
                else:
                    flash(f'Payment method {method} not found', 'error')
        
        elif action == 'add_parent_account':
            parent_account = request.form.get('parent_account_name', '').strip()
            if parent_account:
                if transaction_manager.add_parent_account(parent_account):
                    flash(f'Added parent account: {parent_account}', 'success')
                else:
                    flash(f'Parent account {parent_account} already exists', 'warning')
            else:
                flash('Parent account name cannot be empty', 'error')
        
        elif action == 'remove_parent_account':
            parent_account = request.form.get('parent_account_to_remove', '').strip()
            if parent_account:
                if transaction_manager.remove_parent_account(parent_account):
                    flash(f'Removed parent account: {parent_account}', 'success')
                else:
                    flash(f'Parent account {parent_account} not found', 'error')
        
        elif action == 'add_sub_account':
            parent_account = request.form.get('parent_account_for_sub', '').strip()
            sub_account = request.form.get('sub_account_name', '').strip()
            if parent_account and sub_account:
                if transaction_manager.add_sub_account(parent_account, sub_account):
                    flash(f'Added sub-account {sub_account} to {parent_account}', 'success')
                else:
                    flash(f'Sub-account {sub_account} already exists in {parent_account}', 'warning')
            else:
                flash('Both parent account and sub-account name are required', 'error')
        
        elif action == 'remove_sub_account':
            parent_account = request.form.get('parent_account_for_sub_remove', '').strip()
            sub_account = request.form.get('sub_account_to_remove', '').strip()
            if parent_account and sub_account:
                if transaction_manager.remove_sub_account(parent_account, sub_account):
                    flash(f'Removed sub-account {sub_account} from {parent_account}', 'success')
                else:
                    flash(f'Sub-account {sub_account} not found in {parent_account}', 'error')
        
        return redirect(url_for('information'))
    
    # Get system statistics
    stats = transaction_manager.get_statistics()
    
    return render_template('information.html',
                         default_person=transaction_manager.default_person,
                         roommates=transaction_manager.roommates,
                         payment_methods=transaction_manager.payment_methods,
                         parent_accounts=transaction_manager.parent_accounts,
                         stats=stats)

@app.route('/input_transaction', methods=['GET', 'POST'])
def input_transaction():
    """Enhanced manual transaction input"""
    if request.method == 'POST':
        try:
            # Get form data
            transaction_data = {
                'date': request.form.get('date', '').strip(),
                'description': request.form.get('description', '').strip(),
                'amount': float(request.form.get('amount', 0)),
                'account': request.form.get('account', '').strip(),
                'who_paid': request.form.get('who_paid', '').strip(),
                'who_will_use': request.form.get('who_will_use', '').strip(),
                'method_of_payment': request.form.get('method_of_payment', '').strip(),
                'type': request.form.get('type', 'expense'),
                'parent_account': request.form.get('parent_account', 'Select')
            }
            
            # Create transaction
            transaction = Transaction(**transaction_data)
            
            # Add to manager
            if transaction_manager.add_transaction(transaction):
                flash('Transaction added successfully', 'success')
                return redirect(url_for('input_transaction'))
            else:
                flash('Failed to add transaction. Please check all fields.', 'error')
        
        except ValueError as e:
            flash(f'Invalid amount: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error adding transaction: {str(e)}', 'error')
    
    return render_template('input_transaction.html',
                         roommates=transaction_manager.roommates,
                         payment_methods=transaction_manager.payment_methods,
                         parent_accounts=transaction_manager.parent_accounts,
                         all_sub_accounts=transaction_manager.get_all_sub_accounts())

@app.route('/delete_transaction/<transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    """Delete transaction via AJAX"""
    try:
        if transaction_manager.delete_transaction(transaction_id):
            return jsonify({'success': True, 'message': 'Transaction deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete transaction'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/update_transaction/<transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
    """Update a transaction"""
    try:
        # Get the update data from the request
        update_data = request.get_json()
        
        # Validate required fields
        if not update_data:
            return jsonify({'success': False, 'message': 'No update data provided'})
        
        # Update the transaction
        success = transaction_manager.update_transaction(transaction_id, **update_data)
        
        if success:
            return jsonify({'success': True, 'message': 'Transaction updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update transaction'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error updating transaction: {str(e)}'})

@app.route('/save_all_changes', methods=['POST'])
def save_all_changes():
    """Save all transaction changes from edit mode"""
    try:
        # Get the updated transactions from the request
        updated_transactions = request.get_json().get('transactions', [])
        
        success_count = 0
        error_count = 0
        
        for transaction_data in updated_transactions:
            transaction_id = transaction_data.get('id')
            if transaction_id:
                # Remove id from the data before updating
                update_data = {k: v for k, v in transaction_data.items() if k != 'id'}
                if transaction_manager.update_transaction(transaction_id, **update_data):
                    success_count += 1
                else:
                    error_count += 1
        
        if error_count == 0:
            return jsonify({
                'success': True, 
                'message': f'Successfully updated {success_count} transactions'
            })
        else:
            return jsonify({
                'success': False, 
                'message': f'Updated {success_count} transactions, {error_count} failed'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error saving changes: {str(e)}'})

@app.route('/export_transactions')
def export_transactions():
    """Export transactions to CSV"""
    try:
        transactions = transaction_manager.transactions
        
        # Create CSV content
        csv_content = "Date,Description,Amount,Account,Who Paid,Who Will Use,Method of Payment,Type,Parent Account\n"
        
        for transaction in transactions:
            csv_content += f"{transaction.date},{transaction.description},{transaction.amount},{transaction.account},{transaction.who_paid},{transaction.who_will_use},{transaction.method_of_payment},{transaction.type},{transaction.parent_account}\n"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write(csv_content)
            temp_file = f.name
        
        return send_file(temp_file, as_attachment=True, download_name='transactions.csv')
    
    except Exception as e:
        flash(f'Error exporting transactions: {str(e)}', 'error')
        return redirect(url_for('all_transactions'))

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for real-time statistics"""
    try:
        stats = transaction_manager.get_statistics()
        balances = transaction_manager.calculate_balances()
        week_spending = transaction_manager.get_spending_by_period('week')
        month_spending = transaction_manager.get_spending_by_period('month')
        
        return jsonify({
            'stats': stats,
            'balances': balances,
            'week_spending': week_spending,
            'month_spending': month_spending
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<parent_account>')
def api_sub_accounts(parent_account):
    """API endpoint for getting sub-accounts"""
    try:
        sub_accounts = transaction_manager.get_sub_accounts_for_parent(parent_account)
        return jsonify({'sub_accounts': sub_accounts})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='127.0.0.1')
