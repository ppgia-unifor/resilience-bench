from io import StringIO
import logging
from os import environ
import boto3
from botocore.exceptions import ClientError
import pandas as pd

logger = logging.getLogger()
s3 = boto3.resource('s3')
BUCKET_NAME = environ.get('AWS_BUCKET_NAME')
OUTPUT_PATH = environ.get('OUTPUT_PATH')

def save_file(filename, data, format):
    df = pd.DataFrame(data)
    buffer = StringIO()

    if format == 'csv':
        df.to_csv(buffer, index=False)
        df.to_csv(f'{OUTPUT_PATH}/{filename}.{format}', index=False)
    elif format == 'json':
        df.to_json(buffer)
        df.to_json(f'{OUTPUT_PATH}/{filename}.{format}')
    else:
        raise ValueError(f'format {format} not supported')

    try:
        s3.Object(BUCKET_NAME, f'{OUTPUT_PATH}/{filename}.{format}').put(Body=buffer.getvalue())
        logger.info('File saved in s3')
    except ClientError as e:
        logger.error('File could not be saved in s3')
