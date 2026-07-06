from utils.logger import logger


class GitHubService:

    @staticmethod
    def process_issue(issue_data: dict):

        logger.info(
            f"Issue Received: {issue_data['title']}"
        )

        logger.info(
            f"Repository: {issue_data['repository']}"
        )

        logger.info(
            f"Issue Number: {issue_data['number']}"
        )

        logger.info(
            f"Author: {issue_data['author']}"
        )