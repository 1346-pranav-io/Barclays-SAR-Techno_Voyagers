# SAR Narrative Generator - Technical Architecture

## 🏗️ Architecture Overview

This document provides detailed technical architecture for the SAR Narrative Generator, covering both the current MVP implementation and future AWS scaling.

---

## Current MVP Architecture

### Technology Stack

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│              Streamlit (Frontend)                    │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              Application Layer                       │
│  ┌──────────────────────────────────────────────┐  │
│  │  SAR Generator (sar_generator.py)            │  │
│  │  - Narrative Generation Logic                 │  │
│  │  - Audit Trail Creation                       │  │
│  │  - Risk Pattern Detection                     │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Database Layer (database.py)                 │  │
│  │  - SQLAlchemy ORM                             │  │
│  │  - Data Models                                │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│               External Services                      │
│  ┌────────────────────┐  ┌─────────────────────┐   │
│  │  Anthropic API     │  │  SQLite Database    │   │
│  │  (Claude)          │  │  (Local Storage)    │   │
│  └────────────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Component Details

#### 1. Frontend (Streamlit)
**File**: `app.py`

**Features:**
- Multi-page navigation
- Case data input (manual, upload, sample)
- Narrative display and editing
- Audit trail visualization
- Export functionality

**Key Functions:**
- `main()`: Application entry point
- `show_generate_sar_page()`: Main SAR generation interface
- `display_narrative_section()`: Narrative and audit display
- `show_audit_trail_page()`: System-wide audit logs

#### 2. SAR Generator (Core Logic)
**File**: `sar_generator.py`

**Class**: `SARNarrativeGenerator`

**Key Methods:**
```python
generate_narrative(case_data, customer_data, transaction_data, user)
    → Returns: (narrative_text, audit_trail_dict)
    
_build_context(case_data, customer_data, transaction_data)
    → Analyzes data and builds context
    
_analyze_transactions(transactions)
    → Detects patterns and calculates metrics
    
_identify_risk_indicators(customer_data, transactions, analysis)
    → Identifies suspicious patterns
    
_create_system_prompt()
    → Builds regulatory-compliant system prompt
    
_create_user_prompt(context)
    → Builds case-specific prompt with data
```

**Risk Detection Logic:**
- High volume detection: > 10 unique sources
- Rapid movement: < 24 hours timeframe
- Foreign transfers: International transactions
- Profile inconsistency: Activity vs expected behavior
- Structuring: Multiple amounts near threshold

#### 3. Database Layer
**File**: `database.py`

**Models:**

```python
SARCase
    - case_number (unique identifier)
    - customer_id, customer_name
    - narrative (generated text)
    - raw_data (JSON)
    - risk_score
    - status (draft/reviewed/approved/filed)
    - audit metadata

AuditLog
    - case_number
    - action (generated/edited/approved)
    - user
    - llm_prompt, llm_response
    - data_sources (JSON)
    - reasoning (text)

TransactionAlert
    - alert_id
    - customer_id
    - alert_type
    - transactions (JSON)
    - risk_indicators (JSON)

CustomerProfile
    - customer_id
    - KYC data
    - risk_category
    - previous_sars
```

#### 4. Configuration
**File**: `config.py`

**Settings:**
- API configuration (keys, endpoints)
- Model parameters (temperature, tokens)
- Risk thresholds
- User roles
- Audit settings

---

## Data Flow

### Narrative Generation Flow

```
1. User Input
   └─> Load case data (manual/upload/sample)
   
2. Context Building
   └─> Analyze transactions
   └─> Identify risk indicators
   └─> Build structured context
   
3. Prompt Engineering
   └─> System prompt (regulatory guidelines)
   └─> User prompt (case data + context)
   
4. LLM Processing
   └─> Send to Claude API
   └─> Receive narrative + reasoning
   
5. Audit Trail Creation
   └─> Log all data sources
   └─> Capture LLM reasoning
   └─> Record prompt/response
   └─> Track risk indicators
   
6. Database Storage
   └─> Save SARCase record
   └─> Create AuditLog entry
   
7. User Review
   └─> Display narrative
   └─> Show audit trail
   └─> Enable editing
   
8. Export
   └─> Download narrative (TXT)
   └─> Download audit trail (JSON)
```

### Audit Trail Data Structure

```json
{
  "llm_model": "claude-sonnet-4-20250514",
  "timestamp": "2025-02-15T10:30:00Z",
  "user": "analyst",
  "prompt": "Full user prompt with case data",
  "system_prompt": "Regulatory guidelines and instructions",
  "response": "Generated narrative text",
  "reasoning": "LLM's analytical explanation",
  "data_sources": {
    "customer_data": {...},
    "transaction_count": 48,
    "case_data": {...}
  },
  "risk_indicators_identified": [
    "Multiple sources indicator",
    "Rapid movement indicator",
    "Foreign transfer indicator"
  ],
  "regulatory_references": ["FinCEN", "BSA", "AML"],
  "token_usage": {
    "input_tokens": 2500,
    "output_tokens": 1200
  }
}
```

---

## AWS Migration Architecture

### Phase 1: Cloud Migration

```
┌────────────────────────────────────────────────────────┐
│                      AWS Cloud                          │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Route 53   │→ │   CloudFront │→ │  ALB/API GW │ │
│  └──────────────┘  └──────────────┘  └──────┬──────┘ │
│                                              │         │
│  ┌──────────────────────────────────────────▼──────┐ │
│  │              EC2 / ECS / Lambda                  │ │
│  │         (Streamlit + Application Logic)          │ │
│  └──────────────┬───────────────────────────────────┘ │
│                 │                                      │
│  ┌──────────────▼────────┐  ┌──────────────────────┐ │
│  │   Amazon Bedrock      │  │   Amazon RDS         │ │
│  │   (Claude/Titan)      │  │   (PostgreSQL)       │ │
│  └───────────────────────┘  └──────────────────────┘ │
│                                                        │
│  ┌──────────────────────┐  ┌──────────────────────┐ │
│  │  OpenSearch          │  │  S3                   │ │
│  │  (Vector Store)      │  │  (Document Storage)   │ │
│  └──────────────────────┘  └──────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### Component Mapping

| Current MVP | AWS Service | Purpose |
|-------------|-------------|---------|
| Anthropic API | Amazon Bedrock | LLM inference |
| SQLite | Amazon RDS (PostgreSQL) | Relational database |
| Local storage | Amazon S3 | Document/file storage |
| - | Amazon OpenSearch | Vector search for templates |
| Streamlit (local) | EC2/ECS/Lambda | Application hosting |
| - | CloudWatch | Logging and monitoring |
| - | IAM | Access control |
| - | KMS | Encryption |

### Phase 2: Serverless Architecture

```
User Request
     │
     ▼
API Gateway
     │
     ├─> Lambda (Authenticate)
     │
     ├─> Lambda (Generate Narrative)
     │   ├─> Bedrock (Claude)
     │   ├─> RDS (Get case data)
     │   └─> S3 (Store results)
     │
     ├─> Lambda (Audit Trail)
     │   └─> RDS (Write audit log)
     │
     └─> Lambda (Export)
         └─> S3 (Generate downloads)
```

### Scaling Considerations

**Horizontal Scaling:**
- Multiple Lambda instances for concurrent processing
- RDS read replicas for query performance
- S3 for unlimited storage
- ElastiCache for session/cache data

**Performance Targets:**
- Generate narrative: < 60 seconds
- Load case data: < 2 seconds
- Save to database: < 1 second
- Export: < 5 seconds

**Capacity Planning:**
- 100 concurrent users
- 1000 SARs per day
- 10TB storage (5 years retention)

---

## Security Architecture

### Current MVP Security

1. **API Key Protection**
   - Environment variables
   - Never logged or displayed
   - Rotation recommended

2. **Data Isolation**
   - Local SQLite database
   - No cloud storage
   - User session isolation

3. **Audit Logging**
   - All actions logged
   - User attribution
   - Timestamp tracking

### AWS Security (Future)

```
┌────────────────────────────────────────────┐
│         Security Layers                     │
├────────────────────────────────────────────┤
│  1. Network                                 │
│     - VPC with private subnets              │
│     - Security groups                       │
│     - NACLs                                 │
├────────────────────────────────────────────┤
│  2. Identity & Access                       │
│     - IAM roles and policies                │
│     - SSO integration                       │
│     - MFA enforcement                       │
├────────────────────────────────────────────┤
│  3. Data Protection                         │
│     - KMS encryption at rest                │
│     - TLS 1.3 in transit                    │
│     - S3 bucket policies                    │
├────────────────────────────────────────────┤
│  4. Application                             │
│     - WAF rules                             │
│     - DDoS protection                       │
│     - Rate limiting                         │
├────────────────────────────────────────────┤
│  5. Monitoring                              │
│     - CloudTrail logging                    │
│     - GuardDuty threats                     │
│     - CloudWatch alarms                     │
└────────────────────────────────────────────┘
```

### Role-Based Access Control (RBAC)

| Role | Permissions |
|------|-------------|
| Analyst | Create cases, generate narratives, edit drafts |
| Supervisor | Review, approve, all analyst permissions |
| Compliance Officer | Final approval, export, all permissions |
| Admin | System configuration, user management, all permissions |
| Auditor | Read-only access to all data and audit trails |

---

## Integration Points

### 1. Case Management System Integration

```python
# Example integration
class CaseManagementAdapter:
    def fetch_case(self, case_id):
        # Fetch from case management system
        pass
    
    def update_sar_status(self, case_id, status):
        # Update case status
        pass
    
    def attach_sar(self, case_id, sar_document):
        # Attach generated SAR
        pass
```

### 2. Transaction Monitoring System

```python
# Example webhook handler
@app.post("/webhook/transaction-alert")
def handle_alert(alert_data):
    # Receive alert from TM system
    # Create case in SAR generator
    # Notify analysts
    pass
```

### 3. Regulatory Filing System

```python
# Example FinCEN filing integration
class FinCENAdapter:
    def submit_sar(self, sar_data, audit_trail):
        # Format for FinCEN BSA E-Filing System
        # Submit electronically
        # Track acknowledgment
        pass
```

---

## Performance Optimization

### Current Bottlenecks

1. **LLM API Calls**: 30-60 seconds per narrative
   - Mitigation: Parallel processing for batch
   - Future: Local model deployment

2. **Database Queries**: Minimal impact in MVP
   - Future: Indexing, caching, read replicas

3. **File I/O**: Local SQLite adequate for MVP
   - Future: Network storage, distributed DB

### Optimization Strategies

1. **Caching**
   - Template caching (regulatory language)
   - Customer data caching (session-based)
   - Prompt caching (reuse system prompts)

2. **Batch Processing**
   - Process multiple cases in parallel
   - Queue-based architecture
   - Background job processing

3. **Database Optimization**
   - Index on frequently queried fields
   - Partition large tables
   - Archive old cases

---

## Monitoring & Observability

### Key Metrics

**Application Metrics:**
- Narratives generated per hour/day
- Average generation time
- Success/failure rate
- User activity by role

**System Metrics:**
- API response time
- Database query time
- Error rates
- Resource utilization

**Business Metrics:**
- Time saved per SAR
- Quality scores
- Approval rate
- Regulatory submissions

### Logging Strategy

```python
# Structured logging
{
  "timestamp": "2025-02-15T10:30:00Z",
  "level": "INFO",
  "user": "analyst@bank.com",
  "action": "generate_narrative",
  "case_number": "SAR202502150001",
  "duration_ms": 45000,
  "tokens_used": 3700,
  "status": "success"
}
```

---

## Deployment Strategy

### Development Environment
- Local development with SQLite
- Sample data for testing
- Mock API for offline work

### Staging Environment
- AWS test environment
- Real data (anonymized)
- Integration testing
- User acceptance testing

### Production Environment
- AWS production
- High availability
- Disaster recovery
- Continuous monitoring

### CI/CD Pipeline

```
Code Push
    ↓
GitHub Actions / GitLab CI
    ↓
Automated Tests
    ↓
Build Container
    ↓
Deploy to Staging
    ↓
Automated Tests
    ↓
Manual Approval
    ↓
Deploy to Production
    ↓
Smoke Tests
    ↓
Monitor
```

---

## Cost Estimation (AWS)

### Monthly Costs (Estimated for 1000 SARs/month)

| Service | Usage | Est. Cost |
|---------|-------|-----------|
| Bedrock (Claude) | 1000 requests @ 4K tokens | $120-200 |
| RDS (db.t3.medium) | 24/7 | $50 |
| S3 | 100 GB storage | $2 |
| Lambda | 50K invocations | $5 |
| CloudWatch | Standard logging | $10 |
| **Total** | | **$187-267/month** |

**Cost Optimization:**
- Use Bedrock batch processing
- Right-size RDS instances
- S3 lifecycle policies
- Reserved instances for predictable workloads

---

## Disaster Recovery

### Backup Strategy

1. **Database Backups**
   - RDS automated backups (daily)
   - Point-in-time recovery
   - Cross-region replication

2. **Document Backups**
   - S3 versioning enabled
   - Cross-region replication
   - Glacier for long-term

3. **Configuration**
   - Infrastructure as Code (Terraform/CloudFormation)
   - Version control
   - Documented procedures

### Recovery Objectives

- **RTO** (Recovery Time Objective): 4 hours
- **RPO** (Recovery Point Objective): 1 hour
- **Data Retention**: 7 years (regulatory requirement)

---

## Compliance & Regulations

### Regulatory Requirements

1. **Data Retention**: 7 years minimum
2. **Audit Trail**: Complete, immutable
3. **Access Control**: Role-based, logged
4. **Encryption**: At rest and in transit
5. **Availability**: High availability required

### Compliance Features

- ✅ Complete audit logging
- ✅ User attribution for all actions
- ✅ Immutable audit trail
- ✅ Data encryption
- ✅ Role-based access control
- ✅ Regulatory format compliance

---

## Future Enhancements

### Phase 1 (Months 1-3)
- AWS migration
- Production deployment
- Case management integration

### Phase 2 (Months 4-6)
- Vector database for templates
- Batch processing
- Advanced analytics

### Phase 3 (Months 7-9)
- Multi-language support
- ML-based risk scoring
- Predictive analytics

### Phase 4 (Months 10-12)
- OCR integration
- Mobile application
- API marketplace

---

## Technical Debt & Maintenance

### Current Known Limitations

1. **SQLite**: Not suitable for production scale
   - Migration path: RDS PostgreSQL
   
2. **No caching**: Every request hits LLM
   - Add: Redis/ElastiCache
   
3. **Single model**: Only Claude
   - Add: Model selection, A/B testing
   
4. **No batch processing**: One at a time
   - Add: Queue-based processing

### Maintenance Tasks

- Weekly: Review audit logs
- Monthly: Database optimization
- Quarterly: Security updates
- Annually: Compliance review

---

## Support & Documentation

### Technical Documentation
- API documentation (future)
- Database schema
- Deployment guides
- Troubleshooting guides

### User Documentation
- User manual
- Training materials
- Video tutorials
- FAQ

### Support Tiers
- L1: User questions, basic troubleshooting
- L2: Technical issues, data problems
- L3: Architecture, integration, performance

---

This architecture provides a solid foundation for both the MVP and future scaling to enterprise production use!
