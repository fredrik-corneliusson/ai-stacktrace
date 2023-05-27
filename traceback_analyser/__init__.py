import asyncio
import logging
from typing import AsyncGenerator

from pydantic import BaseModel

from .process_tb import filter_traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

prompt = """
You are a helpful java expert. Here follows a java error traceback where similar lines has been removed for brevity, please provide a helpful summarization in one paragraph and a solution. The solution should be presented in a to the point and compact as possible:
"""

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


async def analyze(trace: str, threshold: float, max_similar_lines: int, temprature: float) -> AsyncGenerator[Message, None]:
    """
    Analyze a Java traceback
    Before being sent for analysis the traceback is filtered to remove unnecessary lines.
    This is to reduce the amount sent to for analysis.
    """
    status = "RUNNING"
    yield Message(status=status, stage="STACKTRACE_FILTERING", message="Filtering traceback...")
    await asyncio.sleep(0)
    processed_trace = filter_traceback(trace, similarity_threshold=threshold, max_similar_lines=max_similar_lines)
    yield Message(status=status, stage="STACKTRACE_FILTRED", message=processed_trace)
    await asyncio.sleep(0)
    yield Message(status=status, stage="ANAYLSIS_RUNNING", message="Analyzing...")
    await asyncio.sleep(0)
    result = send_to_openai_chat(processed_trace, temprature=temprature)
    yield Message(status=status, stage="ANAYLSIS_DONE", message=result.content)
    await asyncio.sleep(0)



instruction = """You are a helpful java expert. Here follows a java error traceback where similar lines has been removed for brevity. Please provide a helpful summarization in one paragraph and a solution. 
The solution should be presented in a to the point and compact as possible:
"""

template = """This is the java traceback:
    >>>
    {traceback}
    >>>
    """

model_name = "gpt-3.5-turbo"


def send_to_openai_chat(traceback: str, temprature=0.0):
    prompt = PromptTemplate(
        input_variables=["traceback"],
        template=template,
    )

    input = {
        "traceback": traceback
    }
    text = prompt.format(**input)

    logger.debug("=== Prompt ===")
    logger.debug(text)
    logger.debug("==============")

    chat = ChatOpenAI(temperature=temprature, model_name=model_name)

    messages = [
        SystemMessage(content=instruction),
        HumanMessage(content=text)
    ]
    return chat(messages)
