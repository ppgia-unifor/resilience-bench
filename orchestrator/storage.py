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

def save_file(filename, data):
    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    try:
        s3.Object(BUCKET_NAME, f'{OUTPUT_PATH}/{filename}.csv').put(Body=csv_buffer.getvalue())
        logger.info('File saved in s3')
    except ClientError as e:
        logger.error('File could not be saved in s3')
