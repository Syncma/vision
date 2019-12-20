import json
import logging
import uuid

from bottle import post, request
from vision.qcp import upload_storage
from vision.models import QiniuStorage
from vision.serializers import storage_serializer


@post('/api/v1/upload')
def upload():

    uploadfile = request.files.get("image")

    content_type = uploadfile.content_type
    image_content = uploadfile.file.read()

    #获取后缀名
    filename = uploadfile.filename
    if "." not in filename:
        suffix = "jpg"
    else:
        suffix = filename.split(".")[-1]

    # 上传到存储
    filename_ = "%s.%s" % (uuid.uuid4().hex, suffix)
    resource_url = upload_storage(filename_, image_content)
    resource_url = "http://" + resource_url

    # 存入数据库
    storage = QiniuStorage.create(
        content_type=content_type,
        path=resource_url,
        size=len(image_content),
    )

    return storage_serializer.dump(storage).data
