"""
SAR Narrative Generator with Audit Trail
"""
import json
from datetime import datetime
from typing import Dict, List, Tuple
import config
from database import AuditLog, SARCase, get_session
import ollama


class SARNarrativeGenerator:
    """Generate SAR narratives with complete audit trail"""


    def __init__(self, api_key: str = None):
    # No API key needed for Ollama (local model)
      self.model = "mistral"   # or "llama3:8b"

        
    def generate_narrative(
        self, 
        case_data: Dict, 
        customer_data: Dict, 
        transaction_data: List[Dict],
        user: str = "system"
    ) -> Tuple[str, Dict]:
        """
        Generate SAR narrative with audit trail
        
        Returns:
            Tuple of (narrative_text, audit_trail_dict)
        """
        # Simulate missing demo data
        customer_data.setdefault("bank", "State Bank of India")
        customer_data.setdefault("location", "Mumbai, India")

        for txn in transaction_data:
            txn.setdefault("destination_country", "United Arab Emirates")
            txn.setdefault("destination_bank", "Emirates NBD")
        # Build context from data
        context = self._build_context(case_data, customer_data, transaction_data)
        
        # Create system prompt
        system_prompt = self._create_system_prompt()
        
        # Create user prompt with data
        user_prompt = self._create_user_prompt(context)
        
        # Log the prompt for audit
        audit_data = {
            "data_sources": {
                "customer_data": customer_data,
                "transaction_count": len(transaction_data),
                "case_data": case_data
            },
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            # Call  Ollama API
            response = ollama.chat(
            model=self.model,
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
    ]
)

            narrative = response["message"]["content"]
            
            # Extract reasoning from response
            reasoning = self._extract_reasoning(narrative)
            
            # Build complete audit trail
            audit_trail = {
               "llm_model": self.model,
               "token_usage": {
                  "input_tokens": 0,
                  "output_tokens": 0
               },
               "risk_indicators_identified": [],
               "regulatory_references": [],
               "data_sources": audit_data["data_sources"],
               "reasoning": "Generated using local Ollama model",
               "system_prompt": system_prompt,
               "prompt": user_prompt,
               "user": user
}

            return narrative, audit_trail
            
        except Exception as e:
            error_audit = {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "user": user
            }
            raise Exception(f"Error generating narrative: {str(e)}") from e
    
    def _build_context(
        self, 
        case_data: Dict, 
        customer_data: Dict, 
        transaction_data: List[Dict]
    ) -> Dict:
        """Build context from input data"""
        
        # Analyze transaction patterns
        transaction_analysis = self._analyze_transactions(transaction_data)
        
        # Identify risk indicators
        risk_indicators = self._identify_risk_indicators(
            customer_data, 
            transaction_data, 
            transaction_analysis
        )
        
        context = {
            "case_number": case_data.get("case_number", "N/A"),
            "customer": customer_data,
            "transactions": transaction_data,
            "transaction_summary": transaction_analysis,
            "risk_indicators": risk_indicators,
            "alert_type": case_data.get("alert_type", "Unknown")
        }
        
        return context
    
    def _analyze_transactions(self, transactions: List[Dict]) -> Dict:
        """Analyze transaction patterns"""
        if not transactions:
            return {}
        
        total_amount = sum(t.get('amount', 0) for t in transactions)
        
        # Count unique sources
        sources = set()
        destinations = set()
        foreign_transfers = 0
        
        for t in transactions:
            if t.get('source'):
                sources.add(t['source'])
            if t.get('destination'):
                destinations.add(t['destination'])
            if t.get('type') == 'international_transfer':
                foreign_transfers += 1
        
        return {
            "total_transactions": len(transactions),
            "total_amount": total_amount,
            "unique_sources": len(sources),
            "unique_destinations": len(destinations),
            "foreign_transfers": foreign_transfers,
            "average_amount": total_amount / len(transactions) if transactions else 0,
            "date_range": self._get_date_range(transactions)
        }
    
    def _identify_risk_indicators(
        self, 
        customer_data: Dict, 
        transactions: List[Dict],
        analysis: Dict
    ) -> List[str]:
        """Identify risk indicators based on patterns"""
        indicators = []
        
        # High volume from multiple sources
        if analysis.get('unique_sources', 0) > config.THRESHOLDS['high_volume_transactions']:
            indicators.append(
                f"Unusually high number of incoming transfers from {analysis['unique_sources']} different sources"
            )
        
        # Rapid movement
        date_range_hours = analysis.get('date_range', {}).get('hours', 0)
        if date_range_hours > 0 and date_range_hours < config.THRESHOLDS['rapid_movement']:
            indicators.append(
                f"Rapid fund movement - all transactions occurred within {date_range_hours} hours"
            )
        
        # Foreign transfers
        if analysis.get('foreign_transfers', 0) > 0:
            indicators.append(
                f"Immediate international transfer of funds - {analysis['foreign_transfers']} foreign transactions"
            )
        
        # Inconsistent with profile
        expected = customer_data.get('expected_activity', '').lower()
        actual = analysis.get('total_amount', 0)
        if 'low' in expected and actual > 100000:
            indicators.append(
                "Transaction volume significantly exceeds customer's expected activity profile"
            )
        
        # Structured deposits
        amounts = [t.get('amount', 0) for t in transactions]
        if self._detect_structuring(amounts):
            indicators.append(
                "Potential structuring - multiple transactions just below reporting threshold"
            )
        
        return indicators
    
    def _detect_structuring(self, amounts: List[float]) -> bool:
        """Detect potential structuring patterns"""
        threshold = config.THRESHOLDS['structured_deposits']
        # Check if multiple amounts are just below threshold
        near_threshold = [a for a in amounts if threshold * 0.8 < a < threshold]
        return len(near_threshold) >= 3
    
    def _get_date_range(self, transactions: List[Dict]) -> Dict:
        """Calculate date range of transactions"""
        if not transactions:
            return {"hours": 0, "days": 0}
        
        dates = [t.get('date') for t in transactions if t.get('date')]
        if not dates:
            return {"hours": 0, "days": 0}
        
        # Simplified - assumes dates are strings or datetime objects
        return {"hours": 168, "days": 7}  # Placeholder
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for SAR narrative generation"""
        return """You are a specialized AI assistant for generating Suspicious Activity Report (SAR) narratives for financial institutions. Your role is to help compliance analysts draft clear, comprehensive, and regulator-ready SAR narratives.

Key Requirements:
1. REGULATORY COMPLIANCE: Follow FinCEN SAR format and BSA/AML requirements
2. CLARITY: Write in clear, professional language suitable for regulatory review
3. OBJECTIVITY: Present facts without bias or speculation
4. COMPLETENESS: Include all relevant details about suspicious activity
5. STRUCTURE: Follow standard SAR narrative format

SAR Narrative Structure:
1. SUBJECT INFORMATION: Customer details and account information
2. SUSPICIOUS ACTIVITY: Description of the suspicious activity and patterns
3. TIMELINE: When the activity occurred
4. AMOUNTS: Transaction amounts and totals
5. INDICATORS: Specific red flags and suspicious indicators
6. INVESTIGATION: Steps taken to investigate
7. CONCLUSION: Summary of why the activity is suspicious

Important Guidelines:
- Be unbiased and do not discriminate based on protected characteristics
- Focus on objective transaction patterns and behaviors
- Reference specific money laundering typologies when applicable
- Include only factual information from provided data
- Explain WHY the activity is suspicious with clear reasoning
- Use professional, formal tone appropriate for regulators

Output Format:
Provide a complete SAR narrative followed by a REASONING section that explains:
- Which data points were most significant
- Which patterns matched known typologies
- Why specific language was chosen
- Regulatory considerations"""

    def _create_user_prompt(self, context: Dict) -> str:
        """Create user prompt with case data"""
        
        prompt = f"""Generate a complete SAR narrative for the following case:

CASE INFORMATION:
Case Number: {context['case_number']}
Alert Type: {context['alert_type']}

CUSTOMER INFORMATION:
Customer ID: {context['customer'].get('customer_id', 'N/A')}
Name: {context['customer'].get('name', 'N/A')}
Account Type: {context['customer'].get('account_type', 'N/A')}
Account Opening Date: {context['customer'].get('account_opening_date', 'N/A')}
Occupation: {context['customer'].get('occupation', 'N/A')}
Expected Activity: {context['customer'].get('expected_activity', 'N/A')}
Risk Category: {context['customer'].get('risk_category', 'N/A')}
Previous SARs: {context['customer'].get('previous_sars', 0)}

TRANSACTION SUMMARY:
Total Transactions: {context['transaction_summary'].get('total_transactions', 0)}
Total Amount: ₹{context['transaction_summary'].get('total_amount', 0):,.2f}
Unique Sources: {context['transaction_summary'].get('unique_sources', 0)}
Unique Destinations: {context['transaction_summary'].get('unique_destinations', 0)}
Foreign Transfers: {context['transaction_summary'].get('foreign_transfers', 0)}

IDENTIFIED RISK INDICATORS:
{chr(10).join('- ' + indicator for indicator in context['risk_indicators'])}

TRANSACTION DETAILS:
{json.dumps(context['transactions'], indent=2)}

Please generate a comprehensive SAR narrative that:
1. Describes the suspicious activity clearly and completely
2. Includes all relevant customer and transaction details
3. Explains why the activity is suspicious
4. References applicable money laundering typologies
5. Maintains professional, regulatory-appropriate tone

After the narrative, provide a REASONING section explaining your analytical approach."""

        return prompt
    
    def _extract_reasoning(self, narrative: str) -> str:
        """Extract reasoning section from narrative"""
        if "REASONING:" in narrative:
            parts = narrative.split("REASONING:")
            if len(parts) > 1:
                return parts[1].strip()
        return "Reasoning not explicitly provided in response"
    
    def _extract_risk_indicators(self, context: Dict) -> List[str]:
        """Extract risk indicators from context"""
        return context.get('risk_indicators', [])
    
    def _extract_regulatory_refs(self, narrative: str) -> List[str]:
        """Extract regulatory references from narrative"""
        refs = []
        keywords = ['FinCEN', 'BSA', 'AML', 'money laundering', 'structuring', 'layering', 'integration']
        for keyword in keywords:
            if keyword.lower() in narrative.lower():
                refs.append(keyword)
        return list(set(refs))
    
    def save_to_database(
        self, 
        case_number: str, 
        narrative: str, 
        audit_trail: Dict, 
        case_data: Dict,
        user: str = "system"
    ):
        """Save SAR case and audit trail to database"""
        session = get_session(config.DB_PATH)
        
        try:
            # Create or update SAR case
            sar_case = session.query(SARCase).filter_by(case_number=case_number).first()
            
            if not sar_case:
                sar_case = SARCase(
                    case_number=case_number,
                    customer_id=case_data.get('customer_id', ''),
                    customer_name=case_data.get('customer_name', ''),
                    narrative=narrative,
                    raw_data=case_data,
                    risk_score=case_data.get('risk_score', 0.0),
                    created_by=user,
                    status='draft'
                )
                session.add(sar_case)
            else:
                sar_case.narrative = narrative
                sar_case.updated_at = datetime.utcnow()
            
            # Create audit log
            audit_log = AuditLog(
                case_number=case_number,
                action='narrative_generated',
                user=user,
                details=audit_trail,
                llm_prompt=audit_trail.get('prompt', ''),
                llm_response=narrative,
                data_sources=audit_trail.get('data_sources', {}),
                reasoning=audit_trail.get('reasoning', '')
            )
            session.add(audit_log)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
