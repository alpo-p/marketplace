import boto3
from os import getenv, path, remove
import uuid

bucket = getenv("BUCKET")
UPLOAD_FOLDER = 'tmp/upload'

def upload_file(path, file_name, bucket):
    '''
    Uploads a file to an S3 bucket
    '''
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(f"{path}/{file_name}", bucket, file_name)

def upload_picture(picture):
    # random pic_name
    pic_name = uuid.uuid4().hex + picture.filename
    pic_path = path.join(UPLOAD_FOLDER, pic_name) 
    picture.save(pic_path)
    upload_file(UPLOAD_FOLDER, pic_name, bucket)
    # remove the temp file
    remove(pic_path)
    return pic_name