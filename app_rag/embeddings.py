from fastembed import TextEmbedding


class EmbeddingModel:

    def __init__(self):

        self.model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

    def embed(self, text: str):

        return next(
            self.model.embed([text])
        )