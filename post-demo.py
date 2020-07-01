# -*- coding: utf-8 -*-
"""
@author: lywen
后台通过接口调用服务，获取OCR识别结果
"""
import base64
import requests
import json
def read_img_base64(f):
    imgString = base64.b64encode(f.read())
    imgString=b'data:image/jpeg;base64,'+imgString
    return imgString.decode()

def post_stream(p,billModel='通用OCR'):
    URL='http://127.0.0.1:8080/ocr'##url地址
    imgString = read_img_base64(p)
    headers = {}
    param      = {'billModel':billModel,##目前支持三种 通用OCR/ 火车票/ 身份证/
                  'imgString':imgString,
                      'textAngle':True

}
    param = json.dumps(param)
    if 1:
            req          =  requests.post(URL,data= param,headers=None,timeout=50)
            data         =  req.content.decode('utf-8')
            data         =  json.loads(data)
    else:
            data =[]
    return data

from PIL import Image
import io

def post_url(url):
    if url[-4:] != ".png":
        raise Exception('only accecpt png!')
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        f = open('/tmp/tmp.png', 'wb')
        for chunk in req:
            f.write(chunk)
        f.close()

        im = Image.open('/tmp/tmp.png')
        rgb_im = im.convert('RGB')
        rgb_im.save('/tmp/tmp.jpeg')
        data = post_stream(open('/tmp/tmp.jpeg', 'rb'))
        data = [d['text'] for d in data['res']]
        return data

if __name__=='__main__':
    import sys
    url = sys.argv[1]
    data = post_url(url)
    print(data)
