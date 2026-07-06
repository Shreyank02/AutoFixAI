from app_rag.embeddings import EmbeddingModel
from app_rag.vector_store import VectorStore


class RepositoryRetriever:

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.store = VectorStore()

    def retrieve(
        self,
        repository,
        issue_text,
        top_k=10,
    ):

        vector = self.embedder.embed(issue_text)

        return self.store.search(

            query_vector=vector.tolist(),

            repository=repository,

            limit=top_k,

        )