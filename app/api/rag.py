from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional

from redis import Redis
import numpy as np
import hashlib

from scripts.vector_utils import embed_text, chunk_text, upsert_redis_vector, search_redis_vector

rag_router = APIRouter()
redis_client = Redis(host="redis", port=6379, decode_responses=True)

class RAGRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

@rag_router.post("/query")
def run_rag(request: RAGRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query is required")

    query_embedding = embed_text(request.query)
    search_results = search_redis_vector(redis_client, query_embedding)
    answer = f"[Mock Answer] Found {len(search_results)} docs for: {request.query}"

    return {
        "answer": answer,
        "sources": [r["id"] for r in search_results]
    }

class Document(BaseModel):
    document_id: str
    content: str

@rag_router.post("/index")
def index_document(doc: Document):
    chunks = chunk_text(doc.content)
    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc.document_id}_chunk_{i}"
        embedding = embed_text(chunk)
        upsert_redis_vector(redis_client, chunk_id, embedding, metadata={"text": chunk, "doc_id": doc.document_id})
    return {"message": f"Indexed {len(chunks)} chunks from document {doc.document_id}"}

@rag_router.post("/reindex/{document_id}")
def reindex_document(document_id: str, content: str = Body(...)):
    # Delete old chunks
    keys = redis_client.keys(f"{document_id}_chunk_*")
    for k in keys:
        redis_client.delete(k)
    # Re-index
    chunks = chunk_text(content)
    for i, chunk in enumerate(chunks):
        chunk_id = f"{document_id}_chunk_{i}"
        embedding = embed_text(chunk)
        upsert_redis_vector(redis_client, chunk_id, embedding, metadata={"text": chunk, "doc_id": document_id})
    return {"message": f"Reindexed {len(chunks)} chunks from document {document_id}"}