import requests
import json
from dotenv import load_dotenv,dotenv_values
import os
def getUrl(request):
    uploaded_file = request.files['file']
    resp={}

    if is_valid_image_file(uploaded_file):
        data = upload_image(uploaded_file.read())

        if data:
            resp['url'] = data
            resp['message']="Success"
            return resp

        resp['url'] = ""
        resp['message'] = "Something wrong from server"
        return resp

    resp['url'] = ""
    resp['message'] = "Wrong file input"
    return resp

def is_valid_image_file(file)-> bool:
    file_name = file.filename
    ext = file_name.split(".")[-1]
    allowed_ext=["jpg","jpeg","png","tif","tiff","gif","heic","svg"]

    if ext.lower() in allowed_ext:
        return True

    return False

def upload_image(file):
    response = get_response(file)

    return response

def get_response(file):
    url = os.environ['a']
    payload = {os.environ['c']: os.environ['b']}
    file = {'file':file}
    response = requests.request("POST", url, data=payload, files=file)

    if response.status_code==200:
        data = response.content
        json_data = data.decode('utf8')
        data_dict = json.loads(json_data)
        url = data_dict.get("url")
        url = url.replace("http://","https://")
        return url

    return