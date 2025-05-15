# Qwen-Agent RAG System with Azure + Helm + Evaluation-Driven Rollout

## 🚀 Deployment (Helm)
```bash
helm upgrade --install qwen-agent ./infra/helm --values infra/helm/values.yaml --set agent.version=v1.0.1
```

## ✅ Evaluation-Based Rollout
New agent versions are deployed **only after**:
- Offline evaluation (LangChain Eval) meets thresholds
- Online feedback (engagement, feedback scores) exceed SLA

## 🧠 Multi-Tenant Support
Each tenant uses:
- Separate Redis namespace (via key prefix)
- Dedicated Vector index + configmap mount
