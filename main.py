#!/usr/bin/env python

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI()
default_models = ["TechWolf/JobBERT-v3"]
st_models = {}
for default_model in default_models:
    st_models["TechWolf/JobBERT-v3"] = SentenceTransformer("TechWolf/JobBERT-v3")


class EmbeddingRequest(BaseModel):
    model: str
    input: str


@app.post("/v1/embeddings")
def generate_embeddings(request: EmbeddingRequest):
    model = request.model
    input = request.input

    st_model = st_models.get(model)
    if st_model is None:
        try:
            st_model = SentenceTransformer(model)
        except Exception as _:
            raise HTTPException(
                status_code=404,
                detail=f"No sentence-transformers model found with name {model}",
            )
        st_models[model] = st_model
    embeddings = st_model.encode(input, normalize_embeddings=True)
    return {
        "object": "list",
        "data": [{"object": "embedding", "index": 0, "embedding": embeddings.tolist()}],
        "model": model,
        # "usage": {"prompt_tokens": 1024, "total_tokens": 1024},
    }
