<<<<<<< HEAD
# SAR Narrative Generator with Audit Trail

## 🎯 Overview

An AI-powered system that generates Suspicious Activity Report (SAR) narratives for financial institutions with complete audit trail and transparency. This MVP combines open-source tools with AWS-ready architecture.

### Key Features

- ✅ **AI-Powered Narrative Generation**: Uses Claude (Anthropic) to generate regulator-ready SAR narratives
- ✅ **Complete Audit Trail**: Tracks every decision, data point, and reasoning step
- ✅ **Interactive UI**: Streamlit-based interface for easy case management
- ✅ **Human-in-the-Loop**: Allows analysts to review, edit, and approve narratives
- ✅ **Risk Pattern Detection**: Automatically identifies suspicious activity patterns
- ✅ **Regulatory Compliance**: Follows FinCEN SAR format and BSA/AML requirements
- ✅ **Data Security**: Role-based access control and audit logging
- ✅ **Hybrid Architecture**: Open-source with AWS integration capability

## 🏗️ Architecture

### Technology Stack

**Open Source Components:**
- **LLM**: Claude (Anthropic API) - Narrative generation
- **Framework**: LangChain - Orchestration
- **Frontend**: Streamlit - Interactive UI
- **Database**: SQLite - Case storage & audit logs
- **Vector DB**: ChromaDB (ready for integration) - Template storage
- **Language**: Python 3.9+

**AWS Integration (Ready):**
- Amazon Bedrock (Claude/Titan) - Alternative LLM backend
- Amazon RDS - Production database
- Amazon S3 - Document storage
- AWS Lambda - Serverless processing
- Amazon OpenSearch - Vector storage

## 📋 Prerequisites

- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- 500MB free disk space
- Internet connection

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
# If you have the files, navigate to the directory
cd sar-narrative-generator
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_actual_api_key_here
```

Or set it directly in the app UI (in the sidebar).

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Configure API Key

1. In the sidebar, enter your Anthropic API key
2. Or set it in the `.env` file

### Step 2: Load a Case

**Option A: Load Example Case (Recommended for first run)**
1. Go to "Generate SAR" tab
2. Click "Load Example Case"
3. Review the case summary showing 47 incoming transfers + 1 outgoing international transfer

**Option B: Upload Your Own Data**
1. Prepare a JSON file with case data (see data format below)
2. Upload via the "Upload Data" tab

### Step 3: Generate SAR Narrative

1. Click "🚀 Generate SAR Narrative"
2. Wait 30-60 seconds for AI processing
3. Review the generated narrative

### Step 4: Review Audit Trail

1. Click on the "🔍 Audit Trail" tab
2. Review:
   - Risk indicators identified
   - Regulatory references
   - Data sources used
   - LLM reasoning
   - Complete prompt/response logs

### Step 5: Edit and Approve

1. Enable "Edit Mode" to modify the narrative
2. Make necessary changes
3. Save changes (tracked in audit trail)
4. Click "✅ Approve SAR" when ready

### Step 6: Export

1. Download narrative as TXT file
2. Download complete audit trail as JSON
3. Ready for regulatory filing!

## 📊 Sample Case Format

The system uses the example from the document: Customer receives ₹50 lakhs from 47 different accounts in one week, then immediately transfers abroad.

### Example Case Structure

```json
{
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
    "account_type": "Savings",
    "occupation": "Business Owner",
    "expected_activity": "Low to moderate transaction volume",
    "risk_category": "Low",
    "previous_sars": 0
  },
  "transactions": [
    {
      "transaction_id": "TXN001",
      "date": "2025-02-08T10:30:00",
      "type": "credit",
      "amount": 95000.00,
      "source": "ACC111111111",
      "destination": "ACC987654321"
    }
    // ... more transactions
  ]
}
```

## 🔒 Security Features

### Data Protection
- ✅ Local SQLite database (no data sent to cloud by default)
- ✅ API keys stored in environment variables
- ✅ No sensitive data in logs
- ✅ Role-based access control ready

### Audit Trail
- ✅ Every action logged with timestamp
- ✅ User attribution for all changes
- ✅ Complete LLM prompt/response tracking
- ✅ Data lineage documentation
- ✅ Reasoning explanations

## 📁 Project Structure

```
sar-narrative-generator/
├── app.py                  # Main Streamlit application
├── sar_generator.py        # Core SAR generation logic
├── database.py             # Database models and operations
├── sample_data.py          # Sample data generator
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── README.md              # This file
└── sar_database.db        # SQLite database (created on first run)
```

## 🎨 Key Features Demonstrated

### 1. Risk Pattern Detection
- Multiple source accounts (structuring indicator)
- Rapid fund movement (< 24 hours)
- Foreign transfers (capital flight risk)
- Inconsistent with customer profile
- Automated threshold detection

### 2. Regulatory Compliance
- FinCEN SAR format
- BSA/AML guidelines
- Money laundering typology references
- Professional regulatory language
- Complete documentation

### 3. Audit Trail Transparency
Every generated narrative includes:
- Which data points influenced the decision
- Why specific language was chosen
- Which patterns were matched
- Regulatory considerations
- Complete prompt engineering details

### 4. Human-in-the-Loop
- Analysts can review AI-generated content
- Edit narratives while maintaining audit trail
- Approve/reject with full accountability
- Track all changes and approvals

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
# Model Configuration
MODEL_NAME = "claude-sonnet-4-20250514"  # Claude model version
TEMPERATURE = 0.3  # Lower = more consistent
MAX_TOKENS = 4000  # Response length

# Risk Thresholds
THRESHOLDS = {
    "high_volume_transactions": 10,
    "rapid_movement": 24,  # hours
    "structured_deposits": 10000,  # INR
    "foreign_transfers": 50000  # INR
}

# Audit Settings
AUDIT_DETAIL_LEVEL = "detailed"  # minimal, standard, detailed
```

## 🔄 Future Enhancements

### Phase 2 - AWS Integration
- [ ] Amazon Bedrock for LLM (multi-model support)
- [ ] Amazon RDS for production database
- [ ] S3 for document storage
- [ ] OpenSearch for vector search
- [ ] Lambda for serverless processing

### Phase 3 - Advanced Features
- [ ] Multi-language support
- [ ] Template library with ChromaDB
- [ ] Batch processing
- [ ] Advanced analytics dashboard
- [ ] Integration with case management systems
- [ ] OCR for document processing

### Phase 4 - Enterprise Features
- [ ] SSO/SAML integration
- [ ] Advanced RBAC
- [ ] Compliance reporting
- [ ] API endpoints
- [ ] Webhook notifications
- [ ] Slack/Teams integration

## 🐛 Troubleshooting

### "API Key Error"
- Ensure your Anthropic API key is valid
- Check you have credits available
- Verify key is correctly set in .env or UI

### "Database Error"
- Delete `sar_database.db` and restart
- Check file permissions
- Ensure SQLite is working

### "Import Errors"
- Verify virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.9+)

### "Streamlit Not Found"
```bash
pip install streamlit
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the example case workflow
3. Verify API key and dependencies

## 📄 License

This is an MVP/Demo project. Customize and extend as needed for your use case.

## ⚖️ Regulatory Disclaimer

This tool assists in SAR narrative drafting but does NOT replace human judgment. All SARs must be reviewed and approved by qualified compliance professionals. Financial institutions remain responsible for regulatory compliance.

## 🙏 Acknowledgments

- Built with Claude (Anthropic)
- Streamlit for the amazing UI framework
- LangChain for LLM orchestration
- Open-source community

---

**Version**: 1.0.0 (MVP)  
**Last Updated**: February 2025  
**Status**: Production-ready MVP
=======
