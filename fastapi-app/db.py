import logging
import os
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

region_name = 'eu-north-1'
dynamodb = boto3.resource('dynamodb', region_name=region_name)

app_env = os.getenv('APP_ENV', 'dev')  # Default to 'dev' if APP_ENV is not set


class UsersDB:
    table_name = f'Stacktrace_Users_{app_env}'

    def __init__(self):
        self._table = dynamodb.Table(self.table_name)
        try:
            self._table.load()
        except dynamodb.meta.client.exceptions.ResourceNotFoundException:
            self._create_db()
        else:
            logger.info(f"OK, Database exists {self.table_name}")

    def _create_db(self):
        logger.info(f"Creating database {self.table_name}")
        self._table = dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

    def get_or_create_user(self, email: str):
        response = self._table.get_item(
            Key={
                'email': email
            }
        )

        if 'Item' not in response:
            logger.info(f'User with email {email} not found, creating...')
            self._table.put_item(
                Item={
                    'email': email,
                    'requests_count': 0,
                    'token_usage': 0
                }
            )
            return {
                'email': email,
                'requests_count': 0,
                'token_usage': 0
            }
        else:
            logger.info(f'User with email {email} found.')
            return response['Item']

    def add_usage(self, email: str, token_usage: int, requests: int = 1):
        response = self._table.update_item(
            Key={
                'email': email
            },
            ExpressionAttributeNames={
                '#requests': 'requests_count',
                '#resource': 'token_usage',
            },
            ExpressionAttributeValues={
                ':inc_req': requests,
                ':inc_res': token_usage,
            },
            UpdateExpression='ADD #requests :inc_req, #resource :inc_res',
            ReturnValues="UPDATED_NEW",
        )
        return response
