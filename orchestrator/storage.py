from io import StringIO
from os import environ
import boto3
from botocore.exceptions import ClientError
import pandas as pd
from pathlib import Path

from logger import get_logger

logger = get_logger('storage')
s3 = boto3.resource('s3')
BUCKET_NAME = environ.get('AWS_BUCKET_NAME')
OUTPUT_PATH = environ.get('OUTPUT_PATH')

def save_file(filename, data, format):
    df = pd.DataFrame(data)
    buffer = StringIO()

    local_path = resolve_local_path(filename, format)
    if format == 'csv':
        df.to_csv(buffer, index=False)
        df.to_csv(local_path, index=False)
    elif format == 'json':
        df.to_json(buffer)
        df.to_json(local_path)
    else:
        raise ValueError(f'format {format} not supported')

    try:
        s3.Object(BUCKET_NAME, f'{OUTPUT_PATH}/{filename}.{format}').put(Body=buffer.getvalue())
        logger.info(f'File saved in s3 at {OUTPUT_PATH}/{filename}.{format}')
    except ClientError as e:
        logger.error('File could not be saved in s3', e)

def resolve_local_path(filename, format):
    path = Path(f'./{OUTPUT_PATH}/{filename}.{format}')
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path.absolute())