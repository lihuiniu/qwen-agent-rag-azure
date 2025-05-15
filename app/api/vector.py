@vector_router.post("/index")
def reindex_documents():
    subprocess.run(["python", "scripts/vector_indexer.py"])
    return {"message": "Vector reindexing complete."}