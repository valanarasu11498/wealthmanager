from datetime import datetime
from typing import List, Dict, Optional
import uuid

class Account:
    def __init__(self, name: str, account_type: str, initial_balance: float = 0.0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.account_type = account_type  # savings, wallet, credit_card
        self.balance = initial_balance
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'account_type': self.account_type,
            'balance': self.balance,
            'created_at': self.created_at.isoformat()
        }

class Transaction:
    def __init__(self, account_id: str, amount: float, transaction_type: str, 
                 category: str, description: str = ""):
        self.id = str(uuid.uuid4())
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type  # income, expense
        self.category = category
        self.description = description
        self.date = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat()
        }

class DataStore:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.categories = [
            'Food', 'Bills', 'Travel', 'Entertainment', 'Shopping', 
            'Healthcare', 'Transportation', 'Education', 'Salary', 'Other'
        ]
        self.account_types = ['savings', 'wallet', 'credit_card']
    
    def add_account(self, name: str, account_type: str, initial_balance: float = 0.0) -> Account:
        account = Account(name, account_type, initial_balance)
        self.accounts[account.id] = account
        return account
    
    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)
    
    def get_all_accounts(self) -> List[Account]:
        return list(self.accounts.values())
    
    def update_account_balance(self, account_id: str, amount: float, transaction_type: str):
        account = self.accounts.get(account_id)
        if account:
            if transaction_type == 'income':
                account.balance += amount
            elif transaction_type == 'expense':
                account.balance -= amount
    
    def add_transaction(self, account_id: str, amount: float, transaction_type: str, 
                       category: str, description: str = "") -> Transaction:
        transaction = Transaction(account_id, amount, transaction_type, category, description)
        self.transactions[transaction.id] = transaction
        self.update_account_balance(account_id, amount, transaction_type)
        return transaction
    
    def get_transactions(self, account_id: str = None, category: str = None, 
                        start_date: datetime = None, end_date: datetime = None) -> List[Transaction]:
        transactions = list(self.transactions.values())
        
        if account_id:
            transactions = [t for t in transactions if t.account_id == account_id]
        
        if category:
            transactions = [t for t in transactions if t.category == category]
        
        if start_date:
            transactions = [t for t in transactions if t.date >= start_date]
        
        if end_date:
            transactions = [t for t in transactions if t.date <= end_date]
        
        return sorted(transactions, key=lambda x: x.date, reverse=True)
    
    def get_total_balance(self) -> float:
        return sum(account.balance for account in self.accounts.values())
    
    def get_category_totals(self) -> Dict[str, float]:
        category_totals = {}
        for transaction in self.transactions.values():
            if transaction.transaction_type == 'expense':
                category_totals[transaction.category] = category_totals.get(transaction.category, 0) + transaction.amount
        return category_totals
    
    def get_account_name(self, account_id: str) -> str:
        account = self.accounts.get(account_id)
        return account.name if account else "Unknown Account"

# Global data store instance
data_store = DataStore()

# Initialize with some default accounts for demonstration
data_store.add_account("Main Savings", "savings", 1000.0)
data_store.add_account("Wallet", "wallet", 200.0)
data_store.add_account("Credit Card", "credit_card", 0.0)
