import openai
import base64
import os
from PIL import Image
import io
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
import re
from datetime import datetime

# Register HEIC plugin for Pillow
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    print("HEIC support enabled")
except ImportError:
    print("HEIC support not available - pillow-heif not installed")

# Load environment variables first
load_dotenv(override=True)

# Debug: Check if API key is loaded correctly
api_key = os.getenv('OPENAI_API_KEY')
print(f"AI Parser - API Key loaded: {api_key[:20] + '...' if api_key and len(api_key) > 20 else api_key}")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

class AITransaction:
    """Enhanced AI transaction model"""
    def __init__(self, date: str = "", description: str = "", amount: float = 0.0, 
                 type: str = "expense", parent_account: str = "Select", ai_id: str = None):
        self.date = date
        self.description = description
        self.amount = amount
        self.type = type
        self.parent_account = parent_account
        self.ai_id = ai_id or f"ai_{hash(f'{datetime.now()}{description}{amount}') % 10000}"
        self.confidence = 0.0  # AI confidence score
        self.raw_text = ""  # Original extracted text

class EnhancedAITransactionParser:
    """Enhanced AI transaction parser with better accuracy and features"""
    
    def __init__(self):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    
    def extract_text_from_image(self, image_path: str) -> Tuple[str, bool]:
        """Extract text from image using OpenAI Vision API with enhanced error handling"""
        try:
            # Handle different image formats
            if image_path.lower().endswith('.heic'):
                # Convert HEIC to JPEG
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save as JPEG in memory
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    img_byte_arr = img_byte_arr.getvalue()
            else:
                # For other formats, read directly
                with open(image_path, 'rb') as image_file:
                    img_byte_arr = image_file.read()
            
            # Encode image to base64
            base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
            
            # Use OpenAI Vision API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Extract ALL text from this image. This could be a receipt, bank statement, or transaction screenshot. 
                                Include ALL visible text, numbers, dates, amounts, and descriptions exactly as they appear. 
                                Preserve the original formatting and structure as much as possible.
                                
                                Focus on:
                                - Transaction dates
                                - Transaction descriptions/merchants
                                - Dollar amounts (both positive and negative)
                                - Account balances
                                - Any transaction IDs or reference numbers
                                
                                Return the complete text extraction."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )
            
            extracted_text = response.choices[0].message.content.strip()
            return extracted_text, True
            
        except Exception as e:
            error_msg = f"Error extracting text: {str(e)}"
            print(error_msg)
            return error_msg, False
    
    def detect_transactions_from_text(self, text: str) -> List[AITransaction]:
        """Enhanced transaction detection with better AI analysis"""
        try:
            # First, classify transaction types and assign parent accounts
            classification_prompt = """
            Analyze the following extracted text and identify ALL financial transactions. 
            
            For each transaction, determine:
            1. Transaction date (extract from text or use today's date if not clear)
            2. Transaction description/merchant name
            3. Amount (negative for expenses/debits, positive for income/credits)
            4. Transaction type (income or expense)
            5. Most likely parent account category from these options:
               - Housing (rent, utilities, internet, furniture)
               - Food (groceries, restaurants, dining, coffee, snacks)
               - Transportation (transit, gas, car insurance, rideshare, bike)
               - Education (tuition, textbooks, supplies)
               - Personal/Lifestyle (clothing, subscriptions, entertainment, hobbies)
               - Health & Wellness (insurance, medication, fitness, haircuts)
               - Savings & Debt (emergency fund, credit payments, loans)
               - Employment (part-time jobs, side hustle)
               - Family Support (allowance, gifts, family help)
               - Loans & Aid (student loans, bursaries, scholarships)
               - Other/Bonus (investments, refunds, selling items)
            
            Important rules:
            - Extract EVERY transaction you can find, even small ones
            - For receipts: ALL amounts are typically expenses (negative)
            - For bank statements: debits are negative, credits are positive
            - If uncertain about parent account, use "Select"
            - Today's date is {current_date}
            
            Return ONLY a JSON array of transactions in this exact format:
            [
                {{
                    "date": "YYYY-MM-DD",
                    "description": "Transaction description",
                    "amount": -XX.XX,
                    "type": "expense",
                    "parent_account": "Category Name",
                    "confidence": 0.95
                }}
            ]
            
            Text to analyze:
            {text}
            """.format(current_date=datetime.now().strftime('%Y-%m-%d'), text=text)
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a financial transaction analysis expert. Extract transactions from text with high accuracy."},
                    {"role": "user", "content": classification_prompt}
                ],
                max_tokens=3000,
                temperature=0.1
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            transactions = []
            try:
                # Clean the response to extract JSON
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    import json
                    transaction_data = json.loads(json_match.group())
                    
                    for item in transaction_data:
                        transaction = AITransaction(
                            date=item.get('date', ''),
                            description=item.get('description', ''),
                            amount=float(item.get('amount', 0)),
                            type=item.get('type', 'expense'),
                            parent_account=item.get('parent_account', 'Select')
                        )
                        transaction.confidence = float(item.get('confidence', 0.8))
                        transaction.raw_text = text
                        transactions.append(transaction)
                
            except json.JSONDecodeError as e:
                print(f"Error parsing AI response as JSON: {e}")
                print(f"Response was: {response_text}")
                
                # Fallback: try to extract transactions manually
                transactions = self._fallback_transaction_extraction(text)
            
            return transactions
            
        except Exception as e:
            print(f"Error in AI transaction detection: {e}")
            return self._fallback_transaction_extraction(text)
    
    def _fallback_transaction_extraction(self, text: str) -> List[AITransaction]:
        """Fallback method to extract transactions when AI parsing fails"""
        transactions = []
        
        # Look for dollar amounts
        amount_pattern = r'\$?([+-]?\d+\.?\d*)'
        amounts = re.findall(amount_pattern, text)
        
        # Look for dates
        date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b'
        dates = re.findall(date_pattern, text)
        
        # Simple extraction logic
        lines = text.split('\n')
        for line in lines:
            if '$' in line or any(char.isdigit() for char in line):
                # Try to extract amount
                amount_match = re.search(r'\$?([+-]?\d+\.?\d*)', line)
                if amount_match:
                    try:
                        amount = float(amount_match.group(1))
                        # Make expenses negative
                        if amount > 0:
                            amount = -abs(amount)
                        
                        transaction = AITransaction(
                            date=dates[0] if dates else datetime.now().strftime('%Y-%m-%d'),
                            description=line.strip(),
                            amount=amount,
                            type="expense",
                            parent_account="Select"
                        )
                        transaction.confidence = 0.5  # Lower confidence for fallback
                        transaction.raw_text = text
                        transactions.append(transaction)
                    except ValueError:
                        continue
        
        return transactions
    
    def analyze_transaction_type(self, description: str, amount: float) -> Tuple[str, str]:
        """Enhanced transaction type and parent account analysis"""
        try:
            prompt = f"""
            Analyze this transaction and determine:
            1. Transaction type (income or expense)
            2. Parent account category
            
            Transaction: {description}
            Amount: {amount}
            
            CRITICAL RULES FOR CLASSIFICATION:
            - POSITIVE amounts (+$50.00) are typically INCOME (deposits, transfers in, refunds, salary, payments received)
            - NEGATIVE amounts (-$50.00) are typically EXPENSES (purchases, bills, transfers out, charges)
            - Look for keywords in description:
              * Income keywords: "deposit", "transfer in", "salary", "refund", "credit", "payment received", "income"
              * Expense keywords: "purchase", "payment", "bill", "transfer out", "debit", "charge", "withdrawal"
            - Choose the most appropriate parent account from:
              Housing, Food, Transportation, Education, Personal/Lifestyle, 
              Health & Wellness, Savings & Debt, Employment, Family Support, 
              Loans & Aid, Other/Bonus
            
            Return as JSON: {{"type": "expense", "parent_account": "Food"}}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial categorization expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.1
            )
            
            response_text = response.choices[0].message.content.strip()
            
            try:
                import json
                result = json.loads(response_text)
                return result.get('type', 'expense'), result.get('parent_account', 'Select')
            except json.JSONDecodeError:
                return 'expense', 'Select'
                
        except Exception as e:
            print(f"Error analyzing transaction type: {e}")
            return 'expense', 'Select'
    
    def enhance_transaction_data(self, transaction: AITransaction) -> AITransaction:
        """Enhance transaction data with additional AI analysis"""
        try:
            # Analyze transaction type and parent account
            transaction_type, parent_account = self.analyze_transaction_type(
                transaction.description, transaction.amount
            )
            
            transaction.type = transaction_type
            transaction.parent_account = parent_account
            
            # Improve description if needed
            if len(transaction.description) > 50:
                # Summarize long descriptions
                prompt = f"""
                Summarize this transaction description to be concise but clear:
                {transaction.description}
                
                Return only the summarized description.
                """
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50,
                    temperature=0.1
                )
                
                transaction.description = response.choices[0].message.content.strip()
            
            return transaction
            
        except Exception as e:
            print(f"Error enhancing transaction data: {e}")
            return transaction
    
    def parse_image_for_transactions(self, image_path: str) -> Tuple[List[AITransaction], str, bool]:
        """Main method to parse image and extract transactions"""
        try:
            # Extract text from image
            extracted_text, success = self.extract_text_from_image(image_path)
            
            if not success:
                return [], extracted_text, False
            
            # Detect transactions from text
            transactions = self.detect_transactions_from_text(extracted_text)
            
            # Enhance each transaction
            enhanced_transactions = []
            for transaction in transactions:
                enhanced_transaction = self.enhance_transaction_data(transaction)
                enhanced_transactions.append(enhanced_transaction)
            
            return enhanced_transactions, extracted_text, True
            
        except Exception as e:
            error_msg = f"Error parsing image: {str(e)}"
            print(error_msg)
            return [], error_msg, False
    
    def validate_transaction(self, transaction: AITransaction) -> Tuple[bool, List[str]]:
        """Validate AI transaction data"""
        errors = []
        
        if not transaction.date:
            errors.append("Date is required")
        
        if not transaction.description:
            errors.append("Description is required")
        
        if transaction.amount == 0:
            errors.append("Amount cannot be zero")
        
        if transaction.type not in ['income', 'expense']:
            errors.append("Type must be 'income' or 'expense'")
        
        return len(errors) == 0, errors
    
    def get_parsing_statistics(self, transactions: List[AITransaction]) -> Dict:
        """Get statistics about parsed transactions"""
        if not transactions:
            return {}
        
        total_amount = sum(t.amount for t in transactions)
        avg_confidence = sum(t.confidence for t in transactions) / len(transactions)
        
        type_counts = {}
        parent_account_counts = {}
        
        for transaction in transactions:
            type_counts[transaction.type] = type_counts.get(transaction.type, 0) + 1
            parent_account_counts[transaction.parent_account] = parent_account_counts.get(transaction.parent_account, 0) + 1
        
        return {
            'total_transactions': len(transactions),
            'total_amount': total_amount,
            'average_confidence': avg_confidence,
            'type_distribution': type_counts,
            'parent_account_distribution': parent_account_counts,
            'high_confidence_transactions': len([t for t in transactions if t.confidence > 0.8])
        }
