"""
Database models for SAR Narrative Generator
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class SARCase(Base):
    """SAR Case Model"""
    __tablename__ = 'sar_cases'
    
    id = Column(Integer, primary_key=True)
    case_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(String(50), nullable=False)
    customer_name = Column(String(200))
    filing_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='draft')  # draft, reviewed, approved, filed
    narrative = Column(Text)
    raw_data = Column(JSON)
    risk_score = Column(Float)
    created_by = Column(String(100))
    approved_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    """Audit Trail Model"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    case_number = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String(100))  # narrative_generated, edited, approved, etc.
    user = Column(String(100))
    details = Column(JSON)  # Stores reasoning, data sources, etc.
    llm_prompt = Column(Text)  # The prompt sent to LLM
    llm_response = Column(Text)  # Raw LLM response
    data_sources = Column(JSON)  # Which data influenced the decision
    reasoning = Column(Text)  # Explanation of the decision

class TransactionAlert(Base):
    """Transaction Alert Model"""
    __tablename__ = 'transaction_alerts'
    
    id = Column(Integer, primary_key=True)
    alert_id = Column(String(50), unique=True)
    customer_id = Column(String(50), nullable=False)
    alert_type = Column(String(100))  # rapid_movement, structuring, high_value, etc.
    alert_date = Column(DateTime, default=datetime.utcnow)
    transaction_count = Column(Integer)
    total_amount = Column(Float)
    currency = Column(String(10), default='INR')
    transactions = Column(JSON)  # List of transaction details
    risk_indicators = Column(JSON)  # List of suspicious patterns
    reviewed = Column(Boolean, default=False)

class CustomerProfile(Base):
    """Customer KYC Profile"""
    __tablename__ = 'customer_profiles'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(200))
    account_number = Column(String(50))
    account_type = Column(String(50))
    account_opening_date = Column(DateTime)
    occupation = Column(String(100))
    expected_activity = Column(String(200))
    risk_category = Column(String(50))  # low, medium, high
    kyc_data = Column(JSON)
    previous_sars = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database initialization
def init_db(db_path='sar_database.db'):
    """Initialize database"""
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def get_session(db_path='sar_database.db'):
    """Get database session"""
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    return Session()
