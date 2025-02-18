import asyncio
from lambda_function_async import lambda_handler_async as async_lambda_handler

def lambda_handler(event, context):
    return asyncio.run(async_lambda_handler(event, context))