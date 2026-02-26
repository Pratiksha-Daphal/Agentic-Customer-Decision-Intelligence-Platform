# 🧠 Agentic Customer Decision Intelligence Platform

**Revenue-aware, risk-balanced next-best-action recommendations with explainable AI**

This project is a **production-style agentic decision system** that helps businesses decide **what to do next for a customer — and when to do nothing** by balancing customer value, churn risk, operational constraints, and historical outcomes.

> ⚠️ This is **not a chatbot**.  
> This is a **decision intelligence platform**.

---

## 🎯 Problem Statement

Most analytics systems answer:

> **“What happened?”**

This platform answers:

> **“What should we do next — and why?”**

### Key challenges addressed
- Static, rule-based personalization
- ML models that predict but don’t decide
- Recommendations that ignore churn and operational risk
- Black-box GenAI outputs with no accountability
- Business users overwhelmed by raw metrics

---

## 🚀 What the System Does

For a given customer, the platform:

1. Builds a customer feature snapshot from transactional data  
2. Estimates **Customer Lifetime Value (CLTV)** using PyTorch  
3. Generates candidate actions:
   - Upsell
   - Cross-sell
   - No Action
4. Evaluates:
   - Churn risk
   - Engagement fatigue
   - Delivery / operational risk
5. Retrieves similar historical cases using **FAISS (RAG)**
6. Applies a **risk-adjusted utility function**
7. Enforces a **minimum utility threshold**
8. Produces a **single, explainable next-best action**
9. Presents the decision in a **business-friendly dashboard**

✅ **NO_ACTION is a valid and intentional outcome**

---

## 🧠 High-Level Architecture
<img width="1024" height="1536" alt="Agentic customer decision platform flowchart" src="https://github.com/user-attachments/assets/292e61a1-3824-4f3c-92ae-88667f700f79" />


All components are orchestrated using **LangGraph**, forming a true **multi-agent system** with clear responsibilities.

---

## 🤖 Multi-Agent Design

Each agent has a **single, bounded responsibility**:

| Agent | Responsibility |
|------|----------------|
| Feature Agent | Build customer behavior snapshot |
| CLTV Agent | Estimate long-term customer value |
| Insight Agent | Retrieve similar historical cases (RAG) |
| Recommendation Agent | Propose candidate actions |
| Risk Agent | Assess churn, fatigue, delivery risk |
| Decision Agent | Select best action using utility logic |

Agents communicate via a **shared state**, not prompt chaining.

---

## 🧮 Decision Logic (Business-Safe)

The platform uses a **risk-adjusted, CLTV-weighted utility function**:
utility =
base_score
× (1 − churn_risk)
× (1 − fatigue_risk)
× (1 − delivery_risk)
× cltv_weight


A **minimum utility threshold** is enforced:

- If expected upside is too small → `NO_ACTION`
- Prevents marginal or harmful outreach

This mirrors how **real enterprise decision systems** operate.

---

## 📡 API Example (Ground Truth)

The API exposes the **raw, auditable decision output**.

- Structured
- Deterministic
- Explainable
- Single source of truth
<img width="1108" height="813" alt="final DI output" src="https://github.com/user-attachments/assets/4b2c900a-5745-4955-a9c4-50362107bb76" />

The UI and explanations are **derived from this output**, never the other way around.

---

## 📊 Business Decision Dashboard

The Streamlit dashboard is designed for **business users**, not engineers.
<img width="917" height="866" alt="image" src="https://github.com/user-attachments/assets/1264c481-6236-437e-9511-83cb85fec783" />

### What it shows
- Recommended action
- Decision confidence
- Clear business explanation
- Best-case vs worst-case framing
- Historical context from similar customers
<img width="1917" height="912" alt="st di" src="https://github.com/user-attachments/assets/9add9c29-61c5-4386-91ae-5ea35a917780" />

### Key views
- Dashboard Home
- Recommended Action & Confidence
- Why This Decision Was Made (LLM-generated, business-readable)

### Explanation principles
- Uses actual numeric values
- Explicitly shows uncertainty
- Never hallucinates data
- Avoids technical jargon

---

## 🗣️ Human-Readable AI Explanations (Mistral)

A **Mistral LLM** is used **only for explanation**, never for decision-making.

### Guardrails
- ✅ Decisions are deterministic
- ✅ LLM only translates verified signals
- ✅ Missing data is explicitly labeled
- ❌ No logic delegation to the LLM
- ❌ No hallucinated numbers

This separation ensures **trust, auditability, and safety**.

---

## 📚 Retrieval-Augmented Context (RAG)

Using **FAISS**, the system retrieves similar historical customer cases to add context:

- How similar customers were treated
- What actions were attempted
- High-level outcome patterns

RAG **augments explanations** — it does **not override decisions**.

---

## 🛠 Tech Stack

### Core
- Python 3.10+
- PostgreSQL
- FastAPI
- SQLAlchemy
- LangGraph

### Machine Learning
- PyTorch (CLTV model)
- Scikit-learn (baselines)

### RAG
- FAISS (CPU)
- SentenceTransformers

### LLM
- Mistral (via Ollama, local)

### Frontend
- Streamlit

✅ All components are **100% open source**

---

## 🚀 How to Run

### 1️⃣ Start the API
```bash
uvicorn app.main:app --reload
streamlit run dashboard/app.py
Enter a customer ID to view the recommendation.
