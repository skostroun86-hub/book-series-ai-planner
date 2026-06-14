from sentence_transformers import SentenceTransformer
from app.config import settings
import numpy as np
from typing import List

model = SentenceTransformer(settings.embedding_model)

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for texts"""
    embeddings = model.encode(texts, convert_to_tensor=False)
    return embeddings.tolist()

def get_embedding(text: str) -> List[float]:
    """Get embedding for single text"""
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()

def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between embeddings"""
    arr1 = np.array(embedding1)
    arr2 = np.array(embedding2)
    return float(np.dot(arr1, arr2) / (np.linalg.norm(arr1) * np.linalg.norm(arr2)))
