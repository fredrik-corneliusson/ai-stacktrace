import asyncio
import logging
from typing import AsyncIterable

from langchain import PromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

from .exceptions import AnalyzeException

VERBOSE_CHAT_LOGGING = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Analyser:
    instruction = """You are a helpful programming java expert. Here follows a error traceback where similar lines has been removed for brevity, please provide a helpful summarization in one paragraph and a solution. 
        The solution should be presented to the point and as compact as possible:
        """

    template = """This is the java traceback:
            >>>
            {traceback}
            >>>
            """

    INPUT_MAX_TOKENS = 2000
    OUTPUT_MAX_TOKENS = 1000
    REQUEST_TIMEOUT = 30
    MODEL_NAME = "gpt-3.5-turbo"

    async def send_to_openai_chat(self, traceback: str, temprature=0.0) -> AsyncIterable[str]:
        # async streaming inspiration from:
        # https://gist.github.com/ninely/88485b2e265d852d3feb8bd115065b1a
        prompt = PromptTemplate(
            input_variables=["traceback"],
            template=self.template,
        )

        input = {
            "traceback": traceback
        }
        text = prompt.format(**input)

        logger.debug("=== Prompt ===")
        logger.debug(text)
        logger.debug("==============")

        callback = AsyncIteratorCallbackHandler()

        chat = ChatOpenAI(
            streaming=True,
            verbose=VERBOSE_CHAT_LOGGING,
            callbacks=[callback],
            temperature=temprature,
            model_name=self.MODEL_NAME,
            request_timeout=self.REQUEST_TIMEOUT,
            max_tokens=self.OUTPUT_MAX_TOKENS)

        messages = [
            SystemMessage(content=self.instruction),
            HumanMessage(content=text)
        ]
        self.input_token_count = chat.get_num_tokens_from_messages(messages)
        if self.input_token_count > self.INPUT_MAX_TOKENS:
            raise AnalyzeException("Input text to large", 413)

        # Begin a task that runs in the background.
        task = asyncio.create_task(chat.agenerate(messages=[messages]))
        self.generated_token_count = 0

        async for token in callback.aiter():
            logger.debug(f"data: {token}")
            self.generated_token_count += 1
            yield token

        await task
        token_usage = self.input_token_count + self.generated_token_count
        logger.info(
            f"Token count: input: {self.input_token_count} generated: {self.generated_token_count} total: {token_usage}")


class AnalyserJava(Analyser):
    instruction = """You are a helpful java expert. Here follows a java error traceback where similar lines has been removed for brevity, please provide a helpful summarization in one paragraph and a solution.
    The solution should be presented to the point and as compact as possible."""

    template = """This is the java traceback:
            >>>
            {traceback}
            >>>
            """


class AnalyserPython(Analyser):
    instruction = """You are a helpful python expert. Here follows a python error traceback where similar lines has been removed for brevity, please provide a helpful summarization in one paragraph and a solution. 
    The solution should be presented to the point and as compact as possible."""

    template = """This is the python traceback:
            >>>
            {traceback}
            >>>
            """
