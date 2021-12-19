from io import StringIO
from os import environ
import boto3
from botocore.exceptions import ClientError
import pandas as pd
from pathlib import Path

from logger import get_logger

logger = get_logger('storage')
BUCKET_NAME = environ.get('AWS_BUCKET_NAME')
OUTPUT_PATH = environ.get('AWS_OUTPUT_PATH')
DISK_PATH = environ.get('DISK_PATH')

def save_file(filename, data, format):
    df = pd.DataFrame(data)
    buffer = StringIO()

    if format == 'csv':
        df.to_csv(buffer, index=False)
    elif format == 'json':
        df.to_json(buffer)
    else:
        raise ValueError(f'format {format} not supported')

    try:
        if BUCKET_NAME:
            s3 = boto3.resource('s3')
            s3.Object(BUCKET_NAME, f'{OUTPUT_PATH}/{filename}.{format}').put(Body=buffer.getvalue())
            logger.info(f'File {OUTPUT_PATH}/{filename}.{format} saved to s3')
        elif DISK_PATH:
            local_path = resolve_local_path(f'{DISK_PATH}/{filename}.{format}')
            with open(local_path, 'w') as file:
                file.write(buffer.getvalue())
            logger.info(f'File {DISK_PATH}/{filename}.{format} saved to disk')
        else:
            logger.error(f'No destination bucket or file path provided to save {filename}.{format}!')      
    except ClientError as e:        
        logger.error(f'File {OUTPUT_PATH}/{filename}.{format} could not be saved to s3', e)
    except OSError as e:
        logger.error(f'File {DISK_PATH}/{filename}.{format} could not be saved to disk', e)    

def resolve_local_path(file_path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path.absolute())