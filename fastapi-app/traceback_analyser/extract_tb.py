import re


def extract_stacktrace(log_data: str) -> str:
    """
    If a stacktrace is copied from a log file, this method can be used to remove the structured logline prefixes
    in order to only get the stacktrace.
    example:
        Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]: Traceback (most recent call last):
        Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/bin/uvicorn", line 8, in <module>
        Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     sys.exit(main())
        Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/click/core.py", line 1130, in __call__
    to:
        Traceback (most recent call last):
          File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/bin/uvicorn", line 8, in <module>
            sys.exit(main())
          File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/click/core.py", line 1130, in __call__


    :param log_lines:
    :return:
    """
    log_lines = log_data.strip().splitlines()
    # Replace all numbers with a placeholder
    lines_with_placeholders = []
    for line in log_lines:
        new_line = re.sub(r'\b\d+\b', '<NUM>', line)
        lines_with_placeholders.append(new_line)

    # Find the common prefix
    common_prefix = _get_common_prefix(lines_with_placeholders)
    print(f"common_prefix: {common_prefix}")

    # Escape special characters in the prefix
    prefix = re.escape(common_prefix)

    # Replace placeholders with regex patterns
    prefix = prefix.replace('<NUM>', r'\b\d+\b')

    # Create a compiled regex object
    prefix_regex = re.compile('^' + prefix)

    # Remove the prefix from each line in the original logs
    original_logs_without_prefix = [prefix_regex.sub('', line) for line in log_lines]
    return '\n'.join(original_logs_without_prefix)


def _get_common_prefix(strs: list[str]) -> str:
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ''
    return prefix

EXAMPLE_TB = """Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]: Traceback (most recent call last):
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/bin/uvicorn", line 8, in <module>
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     sys.exit(main())
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/click/core.py", line 1130, in __call__
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     return self.main(*args, **kwargs)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/click/core.py", line 1055, in main
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     rv = self.invoke(ctx)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/click/core.py", line 1404, in invoke
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     return ctx.invoke(self.callback, **ctx.params)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/click/core.py", line 760, in invoke
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     return __callback(*args, **kwargs)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/uvicorn/main.py", line 410, in main
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     run(
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/uvicorn/main.py", line 578, in run
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     server.run()
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/uvicorn/server.py", line 61, in run
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     return asyncio.run(self.serve(sockets=sockets))
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/usr/lib64/python3.9/asyncio/runners.py", line 44, in run
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     return loop.run_until_complete(main)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "uvloop/loop.pyx", line 1517, in uvloop.loop.Loop.run_until_complete
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/uvicorn/server.py", line 68, in serve
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     config.load()
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/uvicorn/config.py", line 473, in load
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     self.loaded_app = import_from_string(self.app)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/uvicorn/importer.py", line 21, in import_from_string
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     module = importlib.import_module(module_str)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/usr/lib64/python3.9/importlib/__init__.py", line 127, in import_module
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     return _bootstrap._gcd_import(name[level:], package, level)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "<frozen importlib._bootstrap>", line 1030, in _gcd_import
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "<frozen importlib._bootstrap>", line 1007, in _find_and_load
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "<frozen importlib._bootstrap>", line 986, in _find_and_load_unlocked
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "<frozen importlib._bootstrap>", line 680, in _load_unlocked
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "<frozen importlib._bootstrap_external>", line 850, in exec_module
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "<frozen importlib._bootstrap>", line 228, in _call_with_frames_removed
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/app.py", line 18, in <module>
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     from traceback_analyser import analyze, AnalyzeException
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/traceback_analyser/__init__.py", line 62, in <module>
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     user_db = UsersDB()
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/db.py", line 20, in __init__
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     self._table.load()
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/boto3/resources/factory.py", line 564, in do_action
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     response = action(self, *args, **kwargs)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/boto3/resources/action.py", line 88, in __call__
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     response = getattr(parent.meta.client, operation_name)(*args, **params)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/botocore/client.py", line 530, in _api_call
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     return self._make_api_call(operation_name, kwargs)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:   File "/home/ec2-user/projects/ai-stacktrace/fastapi-app/venv/lib64/python3.9/site-packages/botocore/client.py", line 964, in _make_api_call
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]:     raise error_class(parsed_response, operation_name)
Jun 10 16:28:46 ip-172-31-6-210.eu-north-1.compute.internal uvicorn[930113]: botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the DescribeTable operation: User: arn:aws:sts::462854344019:assumed-role/ec2_S3fullacess/i-0bceaf4a808e851f8 is not authorized to perform: dynamodb:DescribeTable on resource: arn:aws:dynamodb:eu-north-1:462854344019:table/Stacktrace_Users_prod because no identity-based policy allows the dynamodb:DescribeTable action

"""

if __name__ == '__main__':
    out = extract_stacktrace(EXAMPLE_TB)
    print(out)
    print('-' * 120)
