import asyncio
import logging
from typing import AsyncGenerator

from pydantic import BaseModel

from .analyser import Analyser, AnalyserJava, AnalyserPython
from .exceptions import AnalyzeException
from .process_tb import FilterTracebackJava

from .quotas import Quotas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DETAILED_RESPONSES = False


class Message(BaseModel):
    status: str
    stage: str
    message: str


quotas = Quotas()


async def analyze(
        user_info: dict,
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
    quotas.check(user_info)

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

    # update token usage
    quotas.add_usage(user_info, analyser)


