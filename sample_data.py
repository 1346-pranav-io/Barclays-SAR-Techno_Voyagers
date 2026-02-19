"""
Sample Data Generator for SAR System Testing
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List
from database import (
    init_db, get_session, CustomerProfile, TransactionAlert, 
    TransactionAlert as Alert
)

class SampleDataGenerator:
    """Generate realistic sample data for SAR testing"""
    
    def __init__(self):
        self.customer_names = [
            "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy",
            "Vikram Singh", "Anita Desai", "Rahul Mehta", "Kavita Nair"
        ]
        
        self.occupations = [
            "Business Owner", "Software Engineer", "Trader", "Consultant",
            "Accountant", "Real Estate Agent", "Doctor", "Entrepreneur"
        ]
        
        self.account_types = ["Savings", "Current", "Business"]
        
    def generate_suspicious_case(self) -> Dict:
        """Generate a suspicious activity case"""
        
        customer_id = f"CUST{random.randint(10000, 99999)}"
        case_number = f"SAR{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        # Customer data
        customer_data = {
            "customer_id": customer_id,
            "name": random.choice(self.customer_names),
            "account_number": f"ACC{random.randint(100000000, 999999999)}",
            "account_type": random.choice(self.account_types),
            "account_opening_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "occupation": random.choice(self.occupations),
            "expected_activity": "Low to moderate transaction volume",
            "risk_category": "Low",
            "previous_sars": 0,
            "kyc_data": {
                "address": "123 MG Road, Mumbai, Maharashtra",
                "phone": "+91-98765-43210",
                "pan": "ABCDE1234F"
            }
        }
        
        # Generate suspicious transaction pattern
        transactions = self._generate_suspicious_transactions()
        
        # Case metadata
        case_data = {
            "case_number": case_number,
            "alert_type": "Rapid Fund Movement - Multiple Sources",
            "customer_id": customer_id,
            "customer_name": customer_data["name"],
            "risk_score": random.uniform(7.5, 9.5)
        }
        
        return {
            "case_data": case_data,
            "customer_data": customer_data,
            "transactions": transactions
        }
    
    def _generate_suspicious_transactions(self) -> List[Dict]:
        """Generate suspicious transaction pattern"""
        
        # Pattern: Multiple incoming transfers followed by large outgoing transfer
        transactions = []
        base_date = datetime.now() - timedelta(days=7)
        
        # Generate 20-50 incoming transfers from different sources
        num_incoming = random.randint(20, 50)
        total_incoming = 0
        
        for i in range(num_incoming):
            amount = random.uniform(50000, 150000)
            total_incoming += amount
            
            transactions.append({
                "transaction_id": f"TXN{random.randint(100000000, 999999999)}",
                "date": (base_date + timedelta(hours=random.randint(0, 48))).isoformat(),
                "type": "credit",
                "amount": round(amount, 2),
                "source": f"ACC{random.randint(100000000, 999999999)}",
                "source_name": f"Account Holder {i+1}",
                "destination": "Customer Account",
                "description": "Fund Transfer",
                "currency": "INR"
            })
        
        # Large outgoing international transfer
        transactions.append({
            "transaction_id": f"TXN{random.randint(100000000, 999999999)}",
            "date": (base_date + timedelta(days=3)).isoformat(),
            "type": "international_transfer",
            "amount": round(total_incoming * 0.95, 2),  # Transfer almost all
            "source": "Customer Account",
            "destination": "Foreign Bank Account",
            "destination_country": "Singapore",
            "description": "International Wire Transfer",
            "currency": "INR"
        })
        
        return transactions
    
    def generate_multiple_cases(self, num_cases: int = 3) -> List[Dict]:
        """Generate multiple sample cases"""
        return [self.generate_suspicious_case() for _ in range(num_cases)]
    
    def seed_database(self):
        """Seed database with sample data"""
        session = get_session()
        
        try:
            # Generate sample cases
            cases = self.generate_multiple_cases(3)
            
            for case in cases:
                customer_data = case['customer_data']
                
                # Add customer profile
                customer = CustomerProfile(
                    customer_id=customer_data['customer_id'],
                    name=customer_data['name'],
                    account_number=customer_data['account_number'],
                    account_type=customer_data['account_type'],
                    account_opening_date=datetime.strptime(
                        customer_data['account_opening_date'], 
                        "%Y-%m-%d"
                    ),
                    occupation=customer_data['occupation'],
                    expected_activity=customer_data['expected_activity'],
                    risk_category=customer_data['risk_category'],
                    kyc_data=customer_data.get('kyc_data', {}),
                    previous_sars=customer_data.get('previous_sars', 0)
                )
                session.add(customer)
                
                # Add transaction alert
                alert = TransactionAlert(
                    alert_id=case['case_data']['case_number'],
                    customer_id=customer_data['customer_id'],
                    alert_type=case['case_data']['alert_type'],
                    transaction_count=len(case['transactions']),
                    total_amount=sum(t['amount'] for t in case['transactions']),
                    transactions=case['transactions'],
                    risk_indicators=[]
                )
                session.add(alert)
            
            session.commit()
            return len(cases)
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# Example case for demo
EXAMPLE_CASE = {
    "case_data": {
        "case_number": "SAR202502150001",
        "alert_type": "Rapid Fund Movement - Multiple Sources",
        "customer_id": "CUST12345",
        "customer_name": "Rajesh Kumar",
        "risk_score": 8.5
    },
    "customer_data": {
        "customer_id": "CUST12345",
        "name": "Rajesh Kumar",
        "account_number": "ACC987654321",
        "account_type": "Savings",
        "account_opening_date": "2020-03-15",
        "occupation": "Business Owner",
        "expected_activity": "Low to moderate transaction volume",
        "risk_category": "Low",
        "previous_sars": 0,
        "kyc_data": {
            "address": "123 MG Road, Mumbai, Maharashtra 400001",
            "phone": "+91-98765-43210",
            "pan": "ABCDE1234F",
            "aadhar": "1234-5678-9012"
        }
    },
    "transactions": [
        {
            "transaction_id": "TXN001",
            "date": "2025-02-08T10:30:00",
            "type": "credit",
            "amount": 95000.00,
            "source": "ACC111111111",
            "source_name": "Ram Mohan",
            "destination": "ACC987654321",
            "description": "Fund Transfer",
            "currency": "INR"
        },
        {
            "transaction_id": "TXN002",
            "date": "2025-02-08T11:15:00",
            "type": "credit",
            "amount": 87000.00,
            "source": "ACC222222222",
            "source_name": "Suresh Pillai",
            "destination": "ACC987654321",
            "description": "Fund Transfer",
            "currency": "INR"
        },
        # ... (abbreviated for space - full example would have 47 transactions)
    ]
}

def get_example_case():
    """Get example case with 47 incoming transfers"""
    case = EXAMPLE_CASE.copy()
    
    # Generate 47 incoming transactions
    transactions = []
    base_date = datetime(2025, 2, 8, 10, 0, 0)
    
    for i in range(47):
        amount = random.uniform(50000, 150000)
        transactions.append({
            "transaction_id": f"TXN{str(i+1).zfill(3)}",
            "date": (base_date + timedelta(hours=i*2)).isoformat(),
            "type": "credit",
            "amount": round(amount, 2),
            "source": f"ACC{random.randint(100000000, 999999999)}",
            "source_name": f"Source Account {i+1}",
            "destination": "ACC987654321",
            "description": "Fund Transfer",
            "currency": "INR"
        })
    
    total_received = sum(t['amount'] for t in transactions)
    
    # Add outgoing international transfer
    transactions.append({
        "transaction_id": "TXN048",
        "date": (base_date + timedelta(days=5)).isoformat(),
        "type": "international_transfer",
        "amount": round(total_received * 0.98, 2),
        "source": "ACC987654321",
        "destination": "FOREIGN-ACC-12345",
        "destination_country": "Singapore",
        "destination_bank": "DBS Bank",
        "description": "International Wire Transfer - Investment",
        "currency": "INR"
    })
    
    case['transactions'] = transactions
    return case
