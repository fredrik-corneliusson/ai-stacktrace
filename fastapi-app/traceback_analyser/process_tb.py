import logging
import re
import textwrap
from pathlib import Path

from Levenshtein import ratio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FilterTraceback:
    def filter(self, traceback: str, similarity_threshold=0.6, max_similar_lines=3, runs=2) -> str:
        pass


class FilterTracebackJava:
    _re_remove_line_nr = re.compile(r':\d+\)$')

    def filter(self, traceback: str, similarity_threshold=0.6, max_similar_lines=3, runs=2) -> str:
        """
        Filter out similar lines to make traceback more compact.
        :param traceback:
        :param similarity_threshold:
        :param max_similar_lines:
        :param runs: Run multiple times to remove any new duplicate lines after a cleanup
        :return: filtred traceback
        """
        logger.info(f"filtering traceback of length {len(traceback)}")
        traceback = textwrap.dedent(traceback)
        traceback = self._remove_file_line_numbers(traceback)
        # remove empty lines
        traceback = '\n'.join(l for l in traceback.splitlines() if l.strip())

        for run in range(runs):
            logger.info(f"run: {run}")
            traceback = self._filter_traceback(traceback, similarity_threshold=similarity_threshold,
                                               max_similar_lines=max_similar_lines)
            logger.info(f"filter traceback length {len(traceback)}")

        return traceback

    def _remove_file_line_numbers(self, traceback: str):
        return '\n'.join(self._re_remove_line_nr.sub(")", line) for line in traceback.splitlines(keepends=False))

    def _filter_traceback(self, traceback: str, similarity_threshold, max_similar_lines) -> str:
        def _similarity(a, b):
            a = self._re_remove_line_nr.sub(")", a)
            b = self._re_remove_line_nr.sub(")", b)
            sim = ratio(a, b)
            logger.debug("--")
            logger.debug(a)
            logger.debug(b)
            logger.debug(sim)
            return sim

        out_lines = []
        last_line = ''
        similar_lines_count = 0
        for line in traceback.splitlines(keepends=False):
            # Check if line contains valuable information, similar to the previous line or '... XXX more'
            # Check if we have already included the max number of similar lines
            if last_line and _similarity(last_line, line) > similarity_threshold:
                similar_lines_count += 1
            else:
                similar_lines_count = 1

            if similar_lines_count <= max_similar_lines:
                out_lines.append(line)

            last_line = line
        filtred_traceback = '\n'.join(out_lines)
        logger.debug(f"filter traceback length {len(filtred_traceback)}")

        return filtred_traceback


class FilterTracebackPython:
    _re_remove_line_nr = re.compile(r', line \d+, ')

    def filter(self, traceback: str, similarity_threshold=0.6, max_similar_lines=3, runs=2) -> str:
        """
        Filter out similar lines to make traceback more compact.
        :param traceback:
        :param similarity_threshold:
        :param max_similar_lines:
        :param runs: Run multiple times to remove any new duplicate lines after a cleanup
        :return: filtred traceback
        """
        logger.info(f"filtering traceback of length {len(traceback)}")
        traceback = textwrap.dedent(traceback)
        traceback = self._remove_file_line_numbers(traceback)
        print(traceback)
        # remove empty lines
        traceback = '\n'.join(l for l in traceback.splitlines() if l.strip())

        for run in range(runs):
            logger.info(f"run: {run}")
            traceback = self._filter_traceback(traceback, similarity_threshold=similarity_threshold,
                                               max_similar_lines=max_similar_lines)
            logger.info(f"filter traceback length {len(traceback)}")

        return traceback

    def _remove_file_line_numbers(self, traceback: str):
        return '\n'.join(self._re_remove_line_nr.sub(", ", line) for line in traceback.splitlines(keepends=False))

    def _filter_traceback(self, traceback: str, similarity_threshold, max_similar_lines) -> str:
        def _similarity(a, b):
            a = self._re_remove_line_nr.sub(")", a)
            b = self._re_remove_line_nr.sub(")", b)
            sim = ratio(a, b)
            logger.debug("--")
            logger.debug(a)
            logger.debug(b)
            logger.debug(sim)
            return sim

        out_lines = []
        last_line = ''
        similar_lines_count = 0
        for line in traceback.splitlines(keepends=False):
            # Check if line contains valuable information, similar to the previous line or '... XXX more'
            # Check if we have already included the max number of similar lines
            if last_line and _similarity(last_line, line) > similarity_threshold:
                similar_lines_count += 1
            else:
                similar_lines_count = 1

            if similar_lines_count <= max_similar_lines:
                out_lines.append(line)

            last_line = line
        filtred_traceback = '\n'.join(out_lines)
        logger.debug(f"filter traceback length {len(filtred_traceback)}")

        return filtred_traceback


if __name__ == '__main__':
    EXAMPLE_TB_JAVA = (Path(__file__).parent.parent.parent / 'sveltekit-app/static/example-tb-java.txt').read_text()

    out = FilterTracebackJava().filter(EXAMPLE_TB_JAVA, similarity_threshold=0.6, max_similar_lines=3)
    print(out)
    print('-' * 120)

    EXAMPLE_TB_PYTHON = (Path(__file__).parent.parent.parent / 'sveltekit-app/static/example-tb-python.txt').read_text()
    out = FilterTracebackJava().filter(EXAMPLE_TB_PYTHON, similarity_threshold=0.6, max_similar_lines=3)
    print(out)
    print('-' * 120)
