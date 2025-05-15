# README.md

# 🔍 Qwen-Agent RAG Platform with Redis 8.0, LangChain Eval, and Azure AKS

A production-ready, multi-tenant Retrieval-Augmented Generation (RAG) agent powered by Qwen-LLM (configurable), Redis 8.0 vector cache, FastAPI, and LangChain Eval. This stack enables:

- 💬 Agent-based RAG with retrain/rerank APIs
- ⚙️ Online + Offline evaluation gates via LangChain Eval
- 📊 Observability with Prometheus + Grafana
- 🔁 Vector index & reindex APIs using Redis ANN
- 🏗️ Helm-based multi-tenant deployment with HPA

---

## 📐 Architecture
See the `docs/qwen_agent_architecture.png` for the full architecture diagram.

```mermaid
graph TD
    A[User] --> B[FastAPI Gateway]
    B --> C[Agent API]
    C --> D[Redis 8.0 Vector Store]
    C --> E[Redis Cache Layer]
    C --> F[LangChain Eval]
    F --> G[Eval Gatekeeper]
    G --> H[Helm Rollout (Per Tenant)]
    C --> I[Feedback API]
    I --> J[Retraining Pipeline]
    J --> K[Model Update Trigger]
    G --> L[Azure Blob (Offline Eval)]
    H --> M[AKS Deployment]
    M --> N[HPA / Service / ConfigMap]
    M --> O[Monitoring (Prometheus + Grafana)]
    subgraph Tenants
        P[agent-v1-tenantA]
        Q[agent-v1-tenantB]
    end
    M --> P
    M --> Q
```

### Core Components
- `FastAPI`: Handles Query, Feedback, Evaluation APIs
- `Redis 8.0`: Stores vectors (using vector similarity index)
- `LangChain Eval`: Scores LLM responses (online + offline)
- `Helm`: Deployment & config templating per tenant
- `Azure`: AKS for Kubernetes, Redis Cache, Blob Storage

---

## Evaluation Flow
See the `docs/qwen_agent_architecture.png` for the full architecture diagram.

```mermaid
graph TD
    A[User Query] --> B[Retrieve Documents (Redis/ANN)]
    B --> C[Agent Response]
    C --> D[LangChain Eval (Online)]
    C --> E[Store for Offline Eval (Blob)]
    D --> F{Pass Eval Gate?}
    F -- Yes --> G[Helm Rollout or Serve]
    F -- No --> H[Hold Deployment]
```

## Feedback Flow
See the `docs/qwen_agent_architecture.png` for the full architecture diagram.

```mermaid
graph TD
    A[User Feedback (Upvote/Downvote/Rating)] --> B[Feedback API]
    B --> C[Store Feedback + Comments]
    C --> D[LangChain Eval Update]
    D --> E[Trigger Retrain Pipeline]
    E --> F[Fine-tuned Model Candidate]
```

## Reindex API Flow
See the `docs/qwen_agent_architecture.png` for the full architecture diagram.

```mermaid
graph TD
    A[Trigger Reindex API] --> B[Fetch Document by ID]
    B --> C[Chunking (Splitter)]
    C --> D[Embed Chunks]
    D --> E[Upsert into Redis 8.0 Vector Store]
```

## 🚀 Deployment Guide

### 1. Prerequisites
- Azure CLI / kubectl
- Helm 3
- Redis 8.0 enabled with vector search (e.g., Azure Redis Enterprise)
- `values.yaml` per tenant

### 2. Build & Push Image
```bash
docker build -t myacr.azurecr.io/qwen-agent:latest .
docker push myacr.azurecr.io/qwen-agent:latest
```

### 3. Deploy per Tenant
```bash
helm upgrade --install agent-tenant-a ./helm/qwen-agent \
  --set tenant=tenant-a \
  --set image.repository=myacr.azurecr.io/qwen-agent \
  --set agent.version=v1

helm upgrade --install agent-tenant-b ./helm/qwen-agent \
  --set tenant=tenant-b \
  --set agent.version=v1 \
  --set enableTraffic=false
```

> ❗ The rollout to production traffic will only happen once the `/gatekeeper/{agent_version}` endpoint returns `"passed": true`

---

## 🔁 Retrain & Reindex APIs

### `/retrain`
Trigger retraining with new feedback data:
```bash
curl -X POST http://localhost:8000/retrain -d '{"agent_version": "v1"}'
```

### `/index`
Index new document chunks with Redis vector cache

### `/reindex/{document_id}`
Replace all vector chunks associated with `document_id`

---
## ✅ Evaluation-Based Rollout
New agent versions are deployed **only after**:
- Offline evaluation (LangChain Eval) meets thresholds:
-- Precision@5 ≥ 0.85
-- Factuality ≥ 0.9
- Online feedback (engagement, feedback scores) exceed SLA
-- Online feedback engagement > 0.9

## ✅ Evaluation Strategies

### Online
- Captures feedback from end-users (ratings, comments)
- Aggregates into LangChain Eval-compatible data
-- Online feedback engagement > 0.9

### Offline
- Batch prompts + reference answers stored in Azure Blob
- Evaluated before rollout
-- Precision@5 ≥ 0.85
-- Factuality ≥ 0.9

### Fallback
- Use top-k keyword search fallback when ANN fails or low score


## ✅ Rollout Strategy
GitHub Actions blocks Helm rollout unless test + eval passes.

---

## 📊 Observability
- `Prometheus`: Metrics exposed via FastAPI instrumented endpoints
```bash
pip install prometheus-fastapi-instrumentator
```
- `Grafana`: Prebuilt dashboard Helm chart `helm/grafana`

---

## 🧠 LLM Model Modes (Configurable)
- Qwen-LLM (default)
- OLLama local models
- PHI-4
- OpenAI GPT

Configurable via `config.yaml`:
```yaml
llm:
  mode: gpt
  model_name: gpt-4
```

---

## 🧪 Tests
```bash
pytest tests/
```

---

## 📁 Project Structure
```
app/
  ├── main.py
  ├── feedback.py
  ├── eval.py
  ├── vector.py
  ├── retrain.py
  └── config.py
scripts/
  └── vector_utils.py
helm/qwen-agent/
docs/
  └── architecture.png
```

---

## 👥 Contributors
Hui

---

For support, open an issue or submit a pull request.