import asyncio
from lambda_function import lambda_handler as async_lambda_handler

def lambda_handler(event, context):
    return asyncio.run(async_lambda_handler(event, context))