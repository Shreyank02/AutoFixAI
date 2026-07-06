from app_rag.retriever import RepositoryRetriever


retriever = RepositoryRetriever()

results = retriever.retrieve(

    repository="licence-plate-detection-and-iot-integration",

    issue_text="""
    Database lookup fails after
    recognizing the license plate.
    """

)
for result in results:

    payload = result.payload

    print("=" * 50)

    print("Score :", result.score)

    print("File  :", payload["file_path"])

    print("Symbol:", payload["symbol"])

    print("Type  :", payload["symbol_type"])