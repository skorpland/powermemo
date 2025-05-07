import numpy as np
from typing import Literal
from ...errors import ExternalAPIError
from ...env import CONFIG, LOG
from .utils import get_jina_async_client_instance

JINA_TASK = {
    "query": "retrieval.query",
    "document": "retrieval.passage",
}


async def jina_embedding(
    model: str, texts: list[str], phase: Literal["query", "document"] = "document"
) -> np.ndarray:
    jina_async_client = get_jina_async_client_instance()
    response = await jina_async_client.post(
        "/embeddings",
        json={
            "model": model,
            "input": texts,
            "task": JINA_TASK[phase],
            "truncate": True,
            "dimensions": CONFIG.embedding_dim,
        },
        timeout=20,
    )
    if response.status_code != 200:
        raise ExternalAPIError(f"Failed to embed texts: {response.text}")
    data = response.json()
    LOG.info(
        f"Jina embedding, {model}, {phase}, {data['usage']['prompt_tokens']}/{data['usage']['total_tokens']}"
    )
    return np.array([dp["embedding"] for dp in data["data"]])
