import base64
import requests
import logging

from bottle import get, abort
from vision.api.baidu import BaiduFace
from vision.auth import check_api_user
from vision.models import QiniuStorage


@get('/api/v1/storages/<storage_id>/detect-face')
def detect_face(storage_id):

    check_api_user()
    storage = QiniuStorage.get(QiniuStorage.id == storage_id)
    url = storage.full_url()
    image_resp = requests.get(url)

    if not image_resp.ok:
        abort(404, 'image not found')

    #人脸检测
    image_content_b64 = base64.b64encode(image_resp.content).decode('utf-8')
    bd_face, is_ok = BaiduFace().detect(image_content_b64)
    if not is_ok:
        abort(500, 'detect exception')

    return bd_face
