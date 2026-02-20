"""
Configuration file for Smart Electricity System
Contains database settings and billing rates
"""

# Database Configuration
DATABASE_CONFIG = {
    'type': 'sqlite',
    'database': 'electricity_system.db',  # SQLite database file
}

# Billing Rate Structure (₹ per unit)
BILLING_RATES = {
    'residential': 5.50,
    'commercial': 7.00,
    'industrial': 6.50
}

BILL_DUE_DAYS = 15  # Days until bill is due