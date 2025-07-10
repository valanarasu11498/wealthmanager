from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app import app
from models import data_store

@app.route('/')
def dashboard():
    """Dashboard with overview of accounts and recent transactions"""
    accounts = data_store.get_all_accounts()
    recent_transactions = data_store.get_transactions()[:10]  # Last 10 transactions
    total_balance = data_store.get_total_balance()
    category_totals = data_store.get_category_totals()
    
    # Add account names to transactions
    for transaction in recent_transactions:
        transaction.account_name = data_store.get_account_name(transaction.account_id)
    
    return render_template('dashboard.html', 
                         accounts=accounts, 
                         recent_transactions=recent_transactions,
                         total_balance=total_balance,
                         category_totals=category_totals)

@app.route('/accounts')
def accounts():
    """Account management page"""
    accounts = data_store.get_all_accounts()
    return render_template('accounts.html', accounts=accounts)

@app.route('/add_account', methods=['POST'])
def add_account():
    """Add a new account"""
    name = request.form.get('name', '').strip()
    account_type = request.form.get('account_type', '')
    initial_balance = float(request.form.get('initial_balance', 0))
    
    if not name:
        flash('Account name is required', 'error')
        return redirect(url_for('accounts'))
    
    if account_type not in data_store.account_types:
        flash('Invalid account type', 'error')
        return redirect(url_for('accounts'))
    
    try:
        data_store.add_account(name, account_type, initial_balance)
        flash(f'Account "{name}" added successfully', 'success')
    except Exception as e:
        flash(f'Error adding account: {str(e)}', 'error')
    
    return redirect(url_for('accounts'))

@app.route('/transactions')
def transactions():
    """Transaction history with filtering"""
    account_id = request.args.get('account_id')
    category = request.args.get('category')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Parse dates
    start_date = None
    end_date = None
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid start date format', 'error')
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            # Set to end of day
            end_date = end_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            flash('Invalid end date format', 'error')
    
    # Get filtered transactions
    transactions = data_store.get_transactions(account_id, category, start_date, end_date)
    
    # Add account names to transactions
    for transaction in transactions:
        transaction.account_name = data_store.get_account_name(transaction.account_id)
    
    accounts = data_store.get_all_accounts()
    categories = data_store.categories
    
    return render_template('transactions.html', 
                         transactions=transactions,
                         accounts=accounts,
                         categories=categories,
                         selected_account=account_id,
                         selected_category=category,
                         start_date=start_date_str,
                         end_date=end_date_str)

@app.route('/add_transaction')
def add_transaction():
    """Add transaction form"""
    accounts = data_store.get_all_accounts()
    categories = data_store.categories
    return render_template('add_transaction.html', accounts=accounts, categories=categories)

@app.route('/add_transaction', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    account_id = request.form.get('account_id')
    amount = request.form.get('amount')
    transaction_type = request.form.get('transaction_type')
    category = request.form.get('category')
    description = request.form.get('description', '').strip()
    
    # Validation
    if not account_id:
        flash('Please select an account', 'error')
        return redirect(url_for('add_transaction'))
    
    if not data_store.get_account(account_id):
        flash('Selected account does not exist', 'error')
        return redirect(url_for('add_transaction'))
    
    try:
        amount = float(amount)
        if amount <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(url_for('add_transaction'))
    except (ValueError, TypeError):
        flash('Invalid amount', 'error')
        return redirect(url_for('add_transaction'))
    
    if transaction_type not in ['income', 'expense']:
        flash('Invalid transaction type', 'error')
        return redirect(url_for('add_transaction'))
    
    if category not in data_store.categories:
        flash('Invalid category', 'error')
        return redirect(url_for('add_transaction'))
    
    try:
        data_store.add_transaction(account_id, amount, transaction_type, category, description)
        flash('Transaction added successfully', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Error adding transaction: {str(e)}', 'error')
        return redirect(url_for('add_transaction'))

@app.route('/api/category_data')
def category_data():
    """API endpoint for category spending data (for charts)"""
    category_totals = data_store.get_category_totals()
    return jsonify(category_totals)

@app.route('/api/account_data')
def account_data():
    """API endpoint for account balance data (for charts)"""
    accounts = data_store.get_all_accounts()
    account_data = {account.name: account.balance for account in accounts}
    return jsonify(account_data)

@app.errorhandler(404)
def not_found(error):
    flash('Page not found', 'error')
    return redirect(url_for('dashboard'))

@app.errorhandler(500)
def internal_error(error):
    flash('An internal error occurred', 'error')
    return redirect(url_for('dashboard'))
