"""
Persistent Storage Manager for Plaid Access Tokens and User Data
Handles saving and loading of Plaid connections across sessions
"""

import os
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class StorageManager:
    """Manages persistent storage for Plaid access tokens and user data"""
    
    def __init__(self, storage_file: str = "plaid_storage.json", encryption_key: str = None):
        """
        Initialize storage manager
        
        Args:
            storage_file: Path to storage file
            encryption_key: Optional encryption key (will generate if not provided)
        """
        self.storage_file = storage_file
        self.encryption_key = encryption_key or self._generate_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        
    def _generate_encryption_key(self) -> str:
        """Generate encryption key from environment or create new one"""
        # Try to get from environment first
        env_key = os.getenv('PLAID_STORAGE_KEY')
        if env_key:
            return env_key.encode()
        
        # Generate new key based on app secret
        app_secret = os.getenv('SECRET_KEY', 'default-secret-key')
        salt = b'luni_plaid_storage_salt'  # Fixed salt for consistency
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(app_secret.encode()))
        return key
    
    def _encrypt_data(self, data: str) -> str:
        """Encrypt data using Fernet encryption"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data using Fernet encryption"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def save_plaid_connection(self, user_id: str, access_token: str, item_id: str, 
                            institution_name: str = None, account_info: Dict = None) -> bool:
        """
        Save Plaid connection data
        
        Args:
            user_id: Unique user identifier
            access_token: Plaid access token
            item_id: Plaid item ID
            institution_name: Name of the financial institution
            account_info: Additional account information
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Load existing data
            storage_data = self.load_storage_data()
            
            # Create connection record
            connection_data = {
                'access_token': access_token,
                'item_id': item_id,
                'institution_name': institution_name or 'Unknown Bank',
                'account_info': account_info or {},
                'created_at': datetime.now().isoformat(),
                'last_used': datetime.now().isoformat(),
                'is_active': True
            }
            
            # Encrypt sensitive data
            encrypted_data = {
                'access_token': self._encrypt_data(access_token),
                'item_id': self._encrypt_data(item_id),
                'institution_name': institution_name or 'Unknown Bank',
                'account_info': account_info or {},
                'created_at': connection_data['created_at'],
                'last_used': connection_data['last_used'],
                'is_active': True
            }
            
            # Store in user's connections
            if 'users' not in storage_data:
                storage_data['users'] = {}
            
            if user_id not in storage_data['users']:
                storage_data['users'][user_id] = {'connections': []}
            
            # Check if connection already exists (by item_id)
            existing_connection = None
            for i, conn in enumerate(storage_data['users'][user_id]['connections']):
                if conn.get('item_id') == encrypted_data['item_id']:
                    existing_connection = i
                    break
            
            if existing_connection is not None:
                # Update existing connection
                storage_data['users'][user_id]['connections'][existing_connection] = encrypted_data
            else:
                # Add new connection
                storage_data['users'][user_id]['connections'].append(encrypted_data)
            
            # Save to file
            self._save_storage_data(storage_data)
            return True
            
        except Exception as e:
            print(f"Error saving Plaid connection: {e}")
            return False
    
    def load_plaid_connections(self, user_id: str) -> List[Dict]:
        """
        Load all Plaid connections for a user
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            List of connection dictionaries
        """
        try:
            storage_data = self.load_storage_data()
            
            if 'users' not in storage_data or user_id not in storage_data['users']:
                return []
            
            connections = []
            for conn in storage_data['users'][user_id].get('connections', []):
                try:
                    # Decrypt sensitive data
                    decrypted_conn = {
                        'access_token': self._decrypt_data(conn['access_token']),
                        'item_id': self._decrypt_data(conn['item_id']),
                        'institution_name': conn['institution_name'],
                        'account_info': conn['account_info'],
                        'created_at': conn['created_at'],
                        'last_used': conn['last_used'],
                        'is_active': conn['is_active']
                    }
                    connections.append(decrypted_conn)
                except Exception as e:
                    print(f"Error decrypting connection: {e}")
                    continue
            
            return connections
            
        except Exception as e:
            print(f"Error loading Plaid connections: {e}")
            return []
    
    def get_active_connection(self, user_id: str) -> Optional[Dict]:
        """
        Get the most recently used active connection
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Active connection dictionary or None
        """
        connections = self.load_plaid_connections(user_id)
        active_connections = [conn for conn in connections if conn.get('is_active', True)]
        
        if not active_connections:
            return None
        
        # Return the most recently used connection
        return max(active_connections, key=lambda x: x.get('last_used', ''))
    
    def update_connection_usage(self, user_id: str, item_id: str) -> bool:
        """
        Update last used timestamp for a connection
        
        Args:
            user_id: Unique user identifier
            item_id: Plaid item ID
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            storage_data = self.load_storage_data()
            
            if 'users' not in storage_data or user_id not in storage_data['users']:
                return False
            
            # Find and update the connection
            for conn in storage_data['users'][user_id]['connections']:
                if conn.get('item_id') == self._encrypt_data(item_id):
                    conn['last_used'] = datetime.now().isoformat()
                    break
            
            self._save_storage_data(storage_data)
            return True
            
        except Exception as e:
            print(f"Error updating connection usage: {e}")
            return False
    
    def deactivate_connection(self, user_id: str, item_id: str) -> bool:
        """
        Deactivate a Plaid connection
        
        Args:
            user_id: Unique user identifier
            item_id: Plaid item ID
            
        Returns:
            True if deactivated successfully, False otherwise
        """
        try:
            storage_data = self.load_storage_data()
            
            if 'users' not in storage_data or user_id not in storage_data['users']:
                return False
            
            # Find and deactivate the connection
            for conn in storage_data['users'][user_id]['connections']:
                if conn.get('item_id') == self._encrypt_data(item_id):
                    conn['is_active'] = False
                    conn['deactivated_at'] = datetime.now().isoformat()
                    break
            
            self._save_storage_data(storage_data)
            return True
            
        except Exception as e:
            print(f"Error deactivating connection: {e}")
            return False
    
    def load_storage_data(self) -> Dict:
        """Load storage data from file"""
        try:
            if not os.path.exists(self.storage_file):
                return {}
            
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading storage data: {e}")
            return {}
    
    def _save_storage_data(self, data: Dict) -> bool:
        """Save storage data to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving storage data: {e}")
            return False
    
    def clear_user_data(self, user_id: str) -> bool:
        """
        Clear all data for a user
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            True if cleared successfully, False otherwise
        """
        try:
            storage_data = self.load_storage_data()
            
            if 'users' in storage_data and user_id in storage_data['users']:
                del storage_data['users'][user_id]
                self._save_storage_data(storage_data)
            
            return True
        except Exception as e:
            print(f"Error clearing user data: {e}")
            return False
