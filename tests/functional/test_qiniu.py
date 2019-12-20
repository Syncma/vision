import webtest


def test_qiniu(app, auth_header, mocker):
    mocker.patch('vision.controllers.qn.upload_storage', return_value="")

    results = app.post('/api/v1/upload', {
        'image': webtest.Upload('test.jpg', b'dummy content'),
    },
                       headers=auth_header)

    assert results.status == '200 OK'
    assert results.json['data']['path'] == "http://"
