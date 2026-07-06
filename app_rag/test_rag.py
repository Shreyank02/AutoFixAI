from app_rag.vector_store import VectorStore
from app_rag.embeddings import EmbeddingModel


store = VectorStore()

store.create_collection()
store.create_payload_indexes()

model = EmbeddingModel()

vector = model.embed(
    "def login(username, password):"
)

print(f"Embedding dimension: {len(vector)}")
print(vector[:10])