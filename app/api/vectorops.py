from fastapi import APIRouter
router = APIRouter()

@router.post("/index")
def index_vectors():
    return {"message": "Vector index updated"}

@router.post("/reindex")
def reindex_all():
    return {"message": "Reindex operation started"}