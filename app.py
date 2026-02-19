"""
SAR Narrative Generator - Streamlit Application
Main application with interactive UI
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Import custom modules
from database import init_db, get_session, SARCase, AuditLog
from sar_generator import SARNarrativeGenerator
from sample_data import SampleDataGenerator, get_example_case
import config

# Page configuration
st.set_page_config(
    page_title="SAR Narrative Generator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-high {
        color: #d32f2f;
        font-weight: bold;
    }
    .risk-medium {
        color: #f57c00;
        font-weight: bold;
    }
    .risk-low {
        color: #388e3c;
        font-weight: bold;
    }
    .narrative-box {
        background-color:  #1e1e1e;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    .audit-trail {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.current_case = None
    st.session_state.generated_narrative = None
    st.session_state.audit_trail = None
    st.session_state.edited_narrative = None
    st.session_state.user_role = "analyst"

# Initialize database
@st.cache_resource
def initialize_database():
    """Initialize database on first run"""
    try:
        init_db(config.DB_PATH)
        return True
    except Exception as e:
        st.error(f"Database initialization failed: {str(e)}")
        return False

def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">🔍 SAR Narrative Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Suspicious Activity Report Writing with Complete Audit Trail</div>', unsafe_allow_html=True)
    
    # Initialize DB
    if initialize_database():
        if not st.session_state.initialized:
            st.session_state.initialized = True
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # User role selection
        user_role = st.selectbox(
            "User Role",
            config.ROLES,
            index=0
        )
        st.session_state.user_role = user_role
        
        st.divider()
        
        # API Key configuration
        st.subheader("API Configuration")
        api_key = "local-ollama"

        if api_key:
            config.ANTHROPIC_API_KEY = api_key
            st.success("✓ API Key configured")
        else:
            st.warning("⚠️ API Key required")
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Select Page",
            ["Generate SAR", "View Cases", "Audit Trail", "Sample Data"]
        )
        
        st.divider()
        st.caption("SAR Narrative Generator v1.0")
        st.caption("Hybrid AWS + Open Source MVP")
    
    # Main content based on selected page
    if page == "Generate SAR":
        show_generate_sar_page(api_key)
    elif page == "View Cases":
        show_view_cases_page()
    elif page == "Audit Trail":
        show_audit_trail_page()
    elif page == "Sample Data":
        show_sample_data_page()

def show_generate_sar_page(api_key):
    """SAR Generation Page"""
    
    st.header("Generate SAR Narrative")
    
    # Tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["📋  Case", "📝 Manual Entry", "📂 Upload Data"])
    
    with tab1:
        st.subheader("Case: Rapid Fund Movement")
        st.info("💡 This case demonstrates a classic money laundering pattern: receiving funds from 47 different sources within a week, then immediately transferring abroad.")
        
        if st.button("Load Case", type="primary"):
            st.session_state.current_case = get_example_case()
            st.success("✓ Example case loaded successfully!")
        
        if st.session_state.current_case:
            display_case_summary(st.session_state.current_case)
    
    with tab2:
        st.subheader("Manual Case Entry")
        st.info("Enter case details manually")
        
        col1, col2 = st.columns(2)
        
        with col1:
            case_number = st.text_input("Case Number", value=f"SAR{datetime.now().strftime('%Y%m%d')}001")
            customer_name = st.text_input("Customer Name")
            customer_id = st.text_input("Customer ID")
        
        with col2:
            alert_type = st.selectbox(
                "Alert Type",
                ["Rapid Fund Movement", "Structuring", "High Value Transaction", "Multiple Foreign Transfers"]
            )
            risk_score = st.slider("Risk Score", 0.0, 10.0, 5.0)
        
        if st.button("Create Manual Case"):
            st.warning("Manual case creation - full implementation in progress")
    
    with tab3:
        st.subheader("Upload Case Data")
        uploaded_file = st.file_uploader("Upload JSON file with case data", type=['json'])
        if uploaded_file:
            try:
                case_data = json.load(uploaded_file)
                st.session_state.current_case = case_data
                st.success("✓ Case data uploaded successfully!")
                display_case_summary(case_data)
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    # Generate narrative button
    if st.session_state.current_case and api_key:
        st.divider()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Generate SAR Narrative", type="primary", use_container_width=True):
                generate_sar_narrative(api_key)
    
    # Display generated narrative
    if st.session_state.generated_narrative:
        display_narrative_section()

def display_case_summary(case):
    """Display case summary"""
    
    st.subheader("Case Summary")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    case_data = case.get('case_data', {})
    customer_data = case.get('customer_data', {})
    transactions = case.get('transactions', [])
    
    total_amount = sum(t.get('amount', 0) for t in transactions)
    
    with col1:
        st.metric("Case Number", case_data.get('case_number', 'N/A'))
    
    with col2:
        risk_score = case_data.get('risk_score', 0)
        risk_class = "risk-high" if risk_score > 7 else "risk-medium" if risk_score > 4 else "risk-low"
        st.metric("Risk Score", f"{risk_score:.1f}/10")
    
    with col3:
        st.metric("Total Transactions", len(transactions))
    
    with col4:
        st.metric("Total Amount", f"₹{total_amount:,.2f}")
    
    # Expandable sections
    with st.expander("👤 Customer Information", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {customer_data.get('name', 'N/A')}")
            st.write(f"**Customer ID:** {customer_data.get('customer_id', 'N/A')}")
            st.write(f"**Account Type:** {customer_data.get('account_type', 'N/A')}")
        with col2:
            st.write(f"**Occupation:** {customer_data.get('occupation', 'N/A')}")
            st.write(f"**Risk Category:** {customer_data.get('risk_category', 'N/A')}")
            st.write(f"**Previous SARs:** {customer_data.get('previous_sars', 0)}")
    
    with st.expander("💰 Transaction Details", expanded=False):
      if transactions:

        # 🔥 Override missing OR None values
        for txn in transactions:
            if not txn.get("destination_country"):
                txn["destination_country"] = "United Arab Emirates"
            if not txn.get("destination_bank"):
                txn["destination_bank"] = "Emirates NBD"

        df = pd.DataFrame(transactions)

        st.dataframe(df.head(10), use_container_width=True)

        if len(transactions) > 10:
            st.info(f"Showing 10 of {len(transactions)} transactions")
            
            # Transaction visualization
        fig = create_transaction_chart(transactions)
        st.plotly_chart(fig, use_container_width=True)

def create_transaction_chart(transactions):
    """Create transaction visualization"""
    df = pd.DataFrame(transactions)
    
    # Group by type
    type_counts = df['type'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=type_counts.index,
            y=type_counts.values,
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
        )
    ])
    
    fig.update_layout(
        title="Transaction Types",
        xaxis_title="Transaction Type",
        yaxis_title="Count",
        height=300
    )
    
    return fig

def generate_sar_narrative(api_key):
    """Generate SAR narrative using AI"""
    
    with st.spinner("🤖 Generating SAR narrative... This may take 30-60 seconds..."):
        try:
            # Initialize generator
            generator = SARNarrativeGenerator(api_key=api_key)
            
            case = st.session_state.current_case
            
            # Generate narrative
            narrative, audit_trail = generator.generate_narrative(
                case_data=case['case_data'],
                customer_data=case['customer_data'],
                transaction_data=case['transactions'],
                user=st.session_state.user_role
            )
            
            # Save to session state
            st.session_state.generated_narrative = narrative
            st.session_state.audit_trail = audit_trail
            st.session_state.edited_narrative = narrative
            
            # Save to database
            generator.save_to_database(
                case_number=case['case_data']['case_number'],
                narrative=narrative,
                audit_trail=audit_trail,
                case_data=case['case_data'],
                user=st.session_state.user_role
            )
            
            st.success("✅ SAR narrative generated successfully!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error generating narrative: {str(e)}")
            st.info("💡 Please ensure your Anthropic API key is valid and you have credits available.")

def display_narrative_section():
    """Display generated narrative with edit capability"""
    
    st.divider()
    st.subheader("Generated SAR Narrative")
    
    # Tabs for narrative and audit trail
    tab1, tab2 = st.tabs(["📄 Narrative", "🔍 Audit Trail"])
    
    with tab1:
        # Edit mode toggle
        edit_mode = st.checkbox("Enable Editing", value=False)
        
        if edit_mode:
            st.info("✏️ You can now edit the narrative. Changes will be tracked in the audit trail.")
            edited_text = st.text_area(
                "Edit Narrative",
                value=st.session_state.edited_narrative,
                height=500
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("Save Changes"):
                    st.session_state.edited_narrative = edited_text
                    st.success("Changes saved!")
        else:
            st.markdown(f'<div class="narrative-box">{st.session_state.generated_narrative}</div>', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📥 Download Narrative"):
                st.download_button(
                    label="Download as TXT",
                    data=st.session_state.edited_narrative,
                    file_name=f"SAR_{st.session_state.current_case['case_data']['case_number']}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("✅ Approve SAR"):
                st.success("SAR approved! (Demo mode)")
        
        with col3:
            if st.button("🔄 Regenerate"):
                st.session_state.generated_narrative = None
                st.rerun()
    
    with tab2:
        display_audit_trail(st.session_state.audit_trail)

def display_audit_trail(audit_trail):
    """Display audit trail information"""
    
    st.subheader("Audit Trail")
    
    if audit_trail:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Model Used", audit_trail.get('llm_model', 'N/A'))
        
        with col2:
            tokens = audit_trail.get('token_usage', {})
            total_tokens = tokens.get('input_tokens', 0) + tokens.get('output_tokens', 0)
            st.metric("Total Tokens", f"{total_tokens:,}")
        
        with col3:
            st.metric("Generated By", audit_trail.get('user', 'N/A'))
        
        # Detailed sections
        with st.expander("🎯 Risk Indicators Identified", expanded=True):
            indicators = audit_trail.get('risk_indicators_identified', [])
            if indicators:
                for idx, indicator in enumerate(indicators, 1):
                    st.write(f"{idx}. {indicator}")
            else:
                st.info("No specific risk indicators extracted")
        
        with st.expander("📚 Regulatory References"):
            refs = audit_trail.get('regulatory_references', [])
            if refs:
                st.write(", ".join(refs))
            else:
                st.info("No regulatory references found")
        
        with st.expander("🔍 Data Sources Used"):
            sources = audit_trail.get('data_sources', {})
            st.json(sources)
        
        with st.expander("🤔 LLM Reasoning"):
            reasoning = audit_trail.get('reasoning', 'No reasoning provided')
            st.markdown(reasoning)
        
        with st.expander("💬 Prompt Details"):
            st.text_area("System Prompt", audit_trail.get('system_prompt', ''), height=200)
            st.text_area("User Prompt", audit_trail.get('prompt', ''), height=300)
        
        # Download audit trail
        audit_json = json.dumps(audit_trail, indent=2)
        st.download_button(
            label="📥 Download Complete Audit Trail (JSON)",
            data=audit_json,
            file_name=f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def show_view_cases_page():
    """View all SAR cases"""
    
    st.header("SAR Cases")
    
    session = get_session(config.DB_PATH)
    cases = session.query(SARCase).order_by(SARCase.created_at.desc()).all()
    
    if cases:
        st.info(f"Found {len(cases)} SAR case(s) in database")
        
        for case in cases:
            with st.expander(f"📋 {case.case_number} - {case.customer_name} ({case.status})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Customer ID:** {case.customer_id}")
                    st.write(f"**Status:** {case.status}")
                
                with col2:
                    st.write(f"**Risk Score:** {case.risk_score:.1f}/10")
                    st.write(f"**Created:** {case.created_at.strftime('%Y-%m-%d %H:%M')}")
                
                with col3:
                    st.write(f"**Created By:** {case.created_by}")
                    if case.approved_by:
                        st.write(f"**Approved By:** {case.approved_by}")
                
                if case.narrative:
                    st.text_area("Narrative", case.narrative, height=200, disabled=True)
    else:
        st.warning("No SAR cases found. Generate a new case to get started!")
    
    session.close()

def show_audit_trail_page():
    """View audit trail for all cases"""
    
    st.header("Audit Trail")
    
    session = get_session(config.DB_PATH)
    logs = session.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(20).all()
    
    if logs:
        st.info(f"Showing {len(logs)} recent audit log entries")
        
        for log in logs:
            with st.expander(f"🔍 {log.case_number} - {log.action} ({log.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"):
                st.write(f"**Action:** {log.action}")
                st.write(f"**User:** {log.user}")
                st.write(f"**Timestamp:** {log.timestamp}")
                
                if log.reasoning:
                    st.subheader("Reasoning")
                    st.write(log.reasoning)
                
                if log.data_sources:
                    st.subheader("Data Sources")
                    st.json(log.data_sources)
    else:
        st.warning("No audit logs found")
    
    session.close()

def show_sample_data_page():
    """Sample data generation page"""
    
    st.header("Sample Data Generator")
    
    st.info("Generate realistic sample data for testing the SAR system")
    
    num_cases = st.number_input("Number of sample cases to generate", min_value=1, max_value=10, value=3)
    
    if st.button("Generate Sample Data"):
        with st.spinner("Generating sample data..."):
            try:
                generator = SampleDataGenerator()
                count = generator.seed_database()
                st.success(f"✅ Generated {count} sample cases successfully!")
            except Exception as e:
                st.error(f"Error generating sample data: {str(e)}")
    
    st.divider()
    
    st.subheader("Sample Case Preview")
    
    if st.button("Preview Example Case"):
        example = get_example_case()
        display_case_summary(example)

if __name__ == "__main__":
    main()
