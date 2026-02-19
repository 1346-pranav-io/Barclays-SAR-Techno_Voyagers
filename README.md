# SAR Narrative Generator with Audit Trail

🎯 Problem Statement:
Financial institutions are required to file Suspicious Activity Reports (SARs) under AML/BSA regulations.

However
⏳ SAR drafting is manual and time-consuming
📜 Regulatory language must be precise and structured
🧾 Every decision must be auditable
📈 Increasing transaction volume strains compliance teams
⚠️ Errors can result in regulatory penalties

Compliance analysts spend 30–60 minutes per SAR, repeating structured regulatory writing under strict oversight.

💡 Our Solution
We built an AI-powered SAR Narrative Generator that:
🔍 Analyzes suspicious transaction patterns
🧠 Detects AML risk indicators
✍️ Generates regulator-ready SAR drafts
📊 Maintains full audit transparency
👩‍⚖️ Keeps humans in control

All processing runs locally using Ollama, ensuring:
🔒 No external API calls
💰 No API costs
🛡 Enterprise-grade data privacy
🌐 Offline capability
🏗 System Architecture
🔹 High-Level Flow

Analyst loads or uploads case data
Risk engine identifies suspicious indicators
Structured context is passed to LLM
Local LLM generates SAR narrative

Audit engine logs:
Risk factors
Prompt details
Model reasoning
Analyst reviews and approves

🔹 Architecture Diagram
                 ┌─────────────────────┐
                 │   Streamlit UI      │
                 │  (Analyst Portal)   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  SAR Generator      │
                 │  (Business Logic)   │
                 └──────────┬──────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Risk Pattern │   │   Ollama LLM    │   │  Audit Engine   │
│ Detection    │   │ (Mistral/Llama) │   │ (Transparency)  │
└──────────────┘   └─────────────────┘   └─────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   SQLite Database   │
                 │  (Cases + Logs)     │
                 └─────────────────────┘

🧠 Key Features
✅ AI-Powered Narrative Generation
Generates regulator-style SAR drafts
Structured AML language
Context-aware suspicious activity explanation

✅ Risk Pattern Detection
Automatically detects:

🔁 Multiple source accounts (structuring)
⏱ Rapid fund movement (< 24 hours)
🌍 Foreign transfers
📊 High transaction volume
👤 Inconsistency with customer profile
✅ Complete Audit Trail

Every SAR includes:
📌 Risk indicators identified
📂 Data sources used
💬 Prompt & model response logs
🧠 Reasoning trace
👤 User attribution
🕒 Timestamp logging
No black-box AI decisions.
✅ Human-in-the-Loop Governance
✏️ Edit mode for analysts
✅ Approval workflow
📝 Change tracking
📤 Export functionality
AI assists — humans decide.
✅ Fully Local AI
🚫 No API keys required
🔒 No external data transmission
🛡 Privacy-preserving
🏢 Enterprise-friendly deployment

📊 Example Use Case

Scenario:
Customer receives ₹50 lakhs
From 47 different accounts
Within one week
Then transfers funds internationally

System identifies:
Multiple-source structuring
Rapid movement pattern
Foreign transfer risk

System generates:
Structured SAR narrative
Suspicious activity explanation
Regulatory-aligned documentation

🚀 How to Run
1️⃣ Install Ollama

Download:
https://ollama.com

Pull a model:

ollama pull mistral


Ensure Ollama is running.

2️⃣ Setup Environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3️⃣ Run Application
streamlit run app.py


Open:

http://localhost:8501

🔒 Responsible AI Design

This system demonstrates:
🧾 Transparent AI reasoning
📊 Traceable decision-making
👩‍⚖️ Mandatory human approval
🔍 Regulatory defensibility
⚖️ Ethical AI deployment
🏆 Hackathon Value Proposition

This project showcases:
🏦 Applied AI in RegTech
🤖 Responsible AI architecture
🛡 Human-in-the-loop governance
📈 Compliance automation
🌍 Real-world financial use case

⚖️ Disclaimer

This system assists SAR drafting but does not replace compliance professionals.
All reports must be reviewed and approved by qualified analysts.