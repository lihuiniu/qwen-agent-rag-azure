import numpy as np
import hashlib

# Placeholder embedding generator
def embed_text(text: str) -> List[float]:
    np.random.seed(int(hashlib.md5(text.encode()).hexdigest(), 16) % 2**32)
    return np.random.rand(1536).tolist()

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def upsert_redis_vector(redis_client, key: str, embedding: List[float], metadata: dict):
    redis_client.hset(key, mapping={"embedding": ",".join(map(str, embedding)), **metadata})

def search_redis_vector(redis_client, query_embedding: List[float], top_k: int = 3):
    all_keys = redis_client.keys("*_chunk_*")
    results = []
    for key in all_keys:
        stored = redis_client.hgetall(key)
        vec = list(map(float, stored.get("embedding", "0," * 1536).split(",")))
        score = np.dot(query_embedding, vec)
        results.append({"id": key, "score": score, "text": stored.get("text")})
    return sorted(results, key=lambda x: -x["score"])[:top_k]
