# Expense & Wealth Manager

## Overview

This is a Flask-based expense and wealth management web application that allows users to track their financial accounts, transactions, and spending patterns. The application features a clean dashboard interface with account management, transaction tracking, and basic financial analytics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Bootstrap 5 with dark theme
- **UI Components**: Responsive web interface using Jinja2 templates
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome for UI icons
- **Theme**: Dark theme optimized for better user experience

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Traditional MVC pattern with separate files for models, routes, and templates
- **Session Management**: Flask sessions with secret key configuration
- **Middleware**: ProxyFix for handling proxy headers in deployment environments

### Data Storage
- **Type**: In-memory storage using Python dictionaries
- **Models**: Object-oriented design with Account and Transaction classes
- **Persistence**: No database persistence - data is lost on application restart
- **Data Store**: Centralized DataStore class managing all data operations

## Key Components

### Core Models
- **Account**: Represents financial accounts (savings, wallet, credit card) with balance tracking
- **Transaction**: Represents financial transactions with categorization and timestamps
- **DataStore**: Central data management class handling all CRUD operations

### Route Structure
- **Dashboard** (`/`): Overview with account summaries, recent transactions, and financial metrics
- **Accounts** (`/accounts`): Account management interface
- **Transactions** (`/transactions`): Transaction history with filtering capabilities
- **Add Transaction** (`/add_transaction`): Form for creating new transactions
- **API Endpoints**: JSON endpoints for chart data

### Template System
- **Base Template**: Common layout with navigation and Bootstrap integration
- **Dashboard**: Main overview with cards and statistics
- **Forms**: Transaction and account creation forms
- **Listings**: Account and transaction list views with filtering

## Data Flow

1. **User Input**: Forms collect account and transaction data
2. **Route Processing**: Flask routes handle form submissions and data validation
3. **Data Storage**: DataStore class manages in-memory data persistence
4. **Template Rendering**: Jinja2 templates render data with Bootstrap styling
5. **Client-Side**: JavaScript handles chart rendering and interactive features

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **Werkzeug**: WSGI utilities and middleware

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme
- **Chart.js**: JavaScript charting library
- **Font Awesome**: Icon library

### Configuration
- **Environment Variables**: Session secret key configuration
- **Logging**: Debug-level logging enabled for development

## Deployment Strategy

### Development Setup
- **Host**: 0.0.0.0 for container compatibility
- **Port**: 5000 (standard Flask development port)
- **Debug Mode**: Enabled for development with auto-reload

### Production Considerations
- **WSGI**: ProxyFix middleware configured for reverse proxy deployment
- **Session Security**: Environment-based secret key configuration
- **Logging**: Configurable logging levels

### Current Limitations
- **Data Persistence**: No database integration - data is volatile
- **Authentication**: No user authentication or authorization
- **Multi-tenancy**: Single-user application design
- **Scalability**: In-memory storage limits scalability

### Recommended Improvements
- **Database Integration**: Add PostgreSQL or SQLite for data persistence
- **User Authentication**: Implement login/logout functionality
- **Data Validation**: Enhanced server-side validation
- **API Documentation**: RESTful API with proper documentation
- **Testing**: Unit and integration test coverage