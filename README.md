# Qwen-Agent RAG System with Azure + Helm + Evaluation-Driven Rollout

## 🚀 Deployment (Helm)
```bash
helm upgrade --install qwen-agent ./infra/helm --values infra/helm/values.yaml --set agent.version=v1.0.1
```

## ✅ Evaluation-Based Rollout
New agent versions are deployed **only after**:
- Offline evaluation (LangChain Eval) meets thresholds:
-- Precision@5 ≥ 0.85
-- Factuality ≥ 0.9
- Online feedback (engagement, feedback scores) exceed SLA
-- Online feedback engagement > 0.9


## ✅ Rollout Strategy
GitHub Actions blocks Helm rollout unless test + eval passes.

## 🚀 Observability (Optional Prometheus Middleware)
```bash
pip install prometheus-fastapi-instrumentator
```

## 🧠 Multi-Tenant Support
Each tenant uses:
- Separate Redis namespace (via key prefix)
- Dedicated Vector index + configmap mount
