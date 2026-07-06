from app_rag.scanner import RepositoryScanner

from app_rag.indexer import RepositoryIndexer


scanner = RepositoryScanner(
    "workspace/repositories/licence-plate-detection-and-iot-integration"
)

context = scanner.scan()

indexer = RepositoryIndexer()

indexer.index_repository(context)