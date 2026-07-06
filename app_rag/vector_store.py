from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
)
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)
from qdrant_client.models import PayloadSchemaType
from core.config import settings


class VectorStore:

    VECTOR_SIZE = 384

    def __init__(self):

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

    def create_collection(self):

        collections = self.client.get_collections()

        names = [
            collection.name
            for collection in collections.collections
        ]

        if settings.QDRANT_COLLECTION in names:

            print("Collection already exists.")

            return

        self.client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=self.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        print("Collection created.")

    def insert(self, points):

        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )

    def search(
        self,
        query_vector,
        repository,
        limit=10,
    ):

        return self.client.query_points(

            collection_name=settings.QDRANT_COLLECTION,

            query=query_vector,

            query_filter=Filter(

                must=[

                    FieldCondition(

                        key="repository",

                        match=MatchValue(
                            value=repository
                        )

                    )

                ]

            ),

            limit=limit,

            with_payload=True,

        ).points
    
    def create_payload_indexes(self):

        self.client.create_payload_index(

            collection_name=settings.QDRANT_COLLECTION,

            field_name="repository",

            field_schema=PayloadSchemaType.KEYWORD,

        )

        print("Repository payload index created.")