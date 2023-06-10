import asyncio
import logging
from typing import AsyncGenerator, AsyncIterable

from langchain.callbacks import AsyncIteratorCallbackHandler
from pydantic import BaseModel

from .process_tb import FilterTracebackJava

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERBOSE_CHAT_LOGGING = False
DETAILED_RESPONSES = False


class Message(BaseModel):
    status: str
    stage: str
    message: str

class AnalyzeException(Exception):
    def __init__(self, message:str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


async def analyze(
        language: str,
        trace: str,
        threshold: float,
        max_similar_lines: int,
        temprature: float) -> AsyncGenerator[Message, None]:
    """
    Analyze a Java traceback
    Before being sent for analysis the traceback is filtered to remove unnecessary lines.
    This is to reduce the amount sent to for analysis.
    """
    logger.debug("analyze...")
    status = "RUNNING"
    if DETAILED_RESPONSES:
        yield Message(status=status, stage="STACKTRACE_FILTERING", message="Filtering traceback...")
        await asyncio.sleep(0)
    processed_trace = FilterTracebackJava().filter(trace, similarity_threshold=threshold,
                                                   max_similar_lines=max_similar_lines)
    if DETAILED_RESPONSES:
        yield Message(status=status, stage="STACKTRACE_FILTRED", message=processed_trace)
        await asyncio.sleep(0)
        yield Message(status=status, stage="ANAYLSIS_RUNNING", message="Analyzing...")
        await asyncio.sleep(0)

    logger.debug("Sending chat prompt and streaming response...")
    if language.lower() == "java":
        analyser = AnalyserJava()
    elif language.lower() == "python":
        analyser = AnalyserPython()
    else:
        # Generic
        analyser = Analyser()

    async for response in analyser.send_to_openai_chat(processed_trace, temprature=temprature):
        yield Message(status="STREAMING_RESPONSE", stage="ANAYLSIS_RUNNING", message=response)

    await asyncio.sleep(0)


class Analyser:
    instruction = """You are a helpful programming java expert. Here follows a error traceback where similar lines has been removed for brevity, please provide a helpful summarization in one paragraph and a solution. 
        The solution should be presented to the point and as compact as possible:
        """

    template = """This is the java traceback:
            >>>
            {traceback}
            >>>
            """

    INPUT_MAX_TOKENS = 3000
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
        input_token_count = chat.get_num_tokens_from_messages(messages)
        if input_token_count > self.INPUT_MAX_TOKENS:
            raise AnalyzeException("Input text to large", 413)

        # Begin a task that runs in the background.
        task = asyncio.create_task(chat.agenerate(messages=[messages]))
        generated_token_count = 0

        async for token in callback.aiter():
            logger.debug(f"data: {token}")
            generated_token_count += 1
            yield token

        await task
        token_usage = input_token_count + generated_token_count
        logger.info(f"Token count: input: {input_token_count} generated: {generated_token_count} total: {token_usage}")


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
