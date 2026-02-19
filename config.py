"""
Configuration for SAR Narrative Generator
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Model Configuration
MODEL_NAME = "claude-sonnet-4-20250514"
MAX_TOKENS = 4000
TEMPERATURE = 0.3  # Lower temperature for consistency

# Database Configuration
DB_PATH = "sar_database.db"
CHROMA_PATH = "./chroma_db"

# SAR Configuration
SAR_TEMPLATES_PATH = "sar_templates"
REGULATORY_GUIDELINES = {
    "FinCEN": "Financial Crimes Enforcement Network",
    "BSA": "Bank Secrecy Act",
    "AML": "Anti-Money Laundering"
}

# Suspicious Activity Thresholds
THRESHOLDS = {
    "high_volume_transactions": 10,
    "rapid_movement": 24,  # hours
    "structured_deposits": 10000,  # currency
    "foreign_transfers": 50000  # currency
}

# User Roles
ROLES = ["analyst", "supervisor", "compliance_officer", "admin"]

# Audit Trail Settings
ENABLE_AUDIT_TRAIL = True
AUDIT_DETAIL_LEVEL = "detailed"  # minimal, standard, detailed
