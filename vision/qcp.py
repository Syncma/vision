import logging

from bottle import default_app
from qiniu import Auth, put_file, put_data

app = default_app()


def get_bucket(bucket_name):
    if bucket_name is None:
        bucket_name = app.config['qiniu.storage.bucket_name']

    return bucket_name


def upload_storage(file_name, data, bucket_name=None):

    bucket = get_bucket(bucket_name)

    ak = app.config['qiniu.storage.access_key']
    sk = app.config['qiniu.storage.secert_key']
    domain = app.config['qiniu.storage.domain_name']

    q = Auth(ak, sk)

    token = q.upload_token(bucket, file_name)
    ret, info = put_data(token, file_name, data)
    logging.info("ret:%s,info:%s", ret, info)

    return '%s/%s' % (domain, file_name)