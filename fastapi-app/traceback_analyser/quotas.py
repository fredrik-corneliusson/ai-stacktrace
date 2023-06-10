import logging

from db import UsersDB
from .analyser import Analyser
from .exceptions import AnalyzeException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_user_db = UsersDB()

class Quotas:
    MAX_TOKEN_USAGE = 40000
    MAX_REQUESTS = 200

    def check(self, user_info):
        user_item = _user_db.get_or_create_user(user_info['email'])
        logger.info(f"user_item: {user_item}")
        if self.MAX_TOKEN_USAGE <= user_item['token_usage']:
            raise AnalyzeException(
                f"Sorry, Token usage quota for user {user_info['email']} reached. Used: {user_item['token_usage']} Limt: {Quotas.MAX_TOKEN_USAGE}",
                413)
        elif self.MAX_REQUESTS <= user_item['requests_count']:
            raise AnalyzeException(
                f"Sorry, Max requests quota for user {user_info['email']} reached. Used: {user_item['requests_count']} Limt: {Quotas.MAX_REQUESTS}",
                413)

    def add_usage(self, user_info, analyser: "Analyser"):
        # update token usage
        add_usage_response = _user_db.add_usage(
            user_info['email'],
            analyser.input_token_count + analyser.generated_token_count)
        logger.info(f"add_usage_response: {add_usage_response}")
