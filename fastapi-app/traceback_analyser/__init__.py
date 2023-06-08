import asyncio
import logging
from typing import AsyncGenerator, AsyncIterable

from langchain.callbacks import AsyncIteratorCallbackHandler
from pydantic import BaseModel

from .process_tb import FilterTracebackJava

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERBOSE_CHAT_LOGGING = False
DETAILED_RESPONSES = False

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)


class Message(BaseModel):
    status: str
    stage: str
    message: str

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
    processed_trace = FilterTracebackJava().filter(trace, similarity_threshold=threshold, max_similar_lines=max_similar_lines)
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


model_name = "gpt-3.5-turbo"



class Analyser:
    instruction = """You are a helpful programming java expert. Here follows a error traceback where similar lines has been removed for brevity, please provide a helpful summarization in one paragraph and a solution. 
        The solution should be presented to the point and as compact as possible:
        """

    template = """This is the java traceback:
            >>>
            {traceback}
            >>>
            """

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
            model_name=model_name)

        messages = [
            SystemMessage(content=self.instruction),
            HumanMessage(content=text)
        ]
        # Begin a task that runs in the background.
        task = asyncio.create_task(chat.agenerate(messages=[messages]))

        async for token in callback.aiter():
            logger.debug(f"data: {token}")
            yield token

        await task

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

