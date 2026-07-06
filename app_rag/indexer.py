from uuid import uuid4

from qdrant_client.models import PointStruct

from app_rag.embeddings import EmbeddingModel

from app_rag.vector_store import VectorStore

from app_rag.chunker import CodeChunker


class RepositoryIndexer:

    def __init__(self):

        self.chunker = CodeChunker()

        self.embedder = EmbeddingModel()

        self.store = VectorStore()

    def index_repository(
        self,
        context,
    ):

        chunks = self.chunker.chunk_repository(
            context
        )

        points = []

        for chunk in chunks:

            vector = self.embedder.embed(
                chunk.embedding_text()
            )

            points.append(

                PointStruct(

                    id=str(uuid4()),

                    vector=vector.tolist(),

                    payload=chunk.model_dump(),

                )

            )

        self.store.insert(points)

        print(

            f"Indexed {len(points)} symbols."

        )