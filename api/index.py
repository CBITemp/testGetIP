import requests
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

TELEGRAPH_URL = 'https://api.openai.com'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    global TELEGRAPH_URL
    url = TELEGRAPH_URL + '/' + path
    headers = dict(request.headers)
    headers['Host'] = TELEGRAPH_URL.replace('https://', '')
    headers['Access-Control-Allow-Origin'] = headers.get('Access-Control-Allow-Origin') or "*"

    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        stream=False)

    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    # Filter out headers not to be forwarded
    excluded_headers = ['content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    # Flatten header list to dictionary
    headers = {name: ", ".join(values) for name, values in headers}

    #return Response(stream_with_context(generate()), response.status_code)
    return Response(response.content, response.status_code)

@app.route("/")
def hello_world():
    return "Connect Success"

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.access_route[-1]

    return jsonify({'ip': ip}), 200

@app.route("/get_outbound_ip", methods=["GET"])
def get_outbound_ip():
    url = "https://xajani9389.pythonanywhere.com/get_my_ip"
    response = requests.get(url)

    result = response.json()
    return result, 200

@app.route("/OpenAIChat", methods=["GET"])
def OpenAIChat():
    target_model = request.args.get("model", "")
    target_prompt = request.args.get("prompt", "")
    APIKey = request.args.get("apikey", "")

    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {APIKey}'
    }
    data = {
        "model": target_model,
        "messages": [
            {"role": "user", "content": target_prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.5,
        "top_p": 1
    }
    try:
        print("start")
        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return "Empty"
    except Exception as e:
        return (str(e))
# from flask import Flask, request, Response, stream_with_context
# import requests
# from flask_cors import CORS



# app = Flask(__name__)
# CORS(app)

# TELEGRAPH_URL = 'https://api.openai.com'

# @app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def proxy(path):
#     global TELEGRAPH_URL
#     url = TELEGRAPH_URL + '/' + path
#     headers = dict(request.headers)
#     headers['Host'] = TELEGRAPH_URL.replace('https://', '')
#     headers['Access-Control-Allow-Origin'] = headers.get('Access-Control-Allow-Origin') or "*"
    
#     response = requests.request(
#         method=request.method,
#         url=url,
#         headers=headers,
#         data=request.get_data(),
#         cookies=request.cookies,
#         allow_redirects=False,
#         stream=False)

#     # def generate():
#     #     for chunk in response.iter_content(chunk_size=1024):
#     #         if chunk:
#     #             yield chunk

#     # Filter out headers not to be forwarded
#     excluded_headers = ['content-length', 'transfer-encoding', 'connection']
#     headers = [(name, value) for (name, value) in response.raw.headers.items()
#                if name.lower() not in excluded_headers]

#     # Flatten header list to dictionary
#     headers = {name: ", ".join(values) for name, values in headers}

#     return Response(response.content, response.status_code)
#     # global TELEGRAPH_URL
#     # target_url  = TELEGRAPH_URL + '/' + path
#     # resp = requests.request(
#     #     method=request.method,
#     #     url=target_url,
#     #     headers={key: value for key, value in request.headers if key != 'Host'},
#     #     data=request.get_data(),
#     #     cookies=request.cookies,
#     #     allow_redirects=False)

#     # # 将从目标 URL 获取的响应返回给客户端
#     # excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#     # headers = [(name, value) for (name, value) in resp.raw.headers.items()
#     #            if name.lower() not in excluded_headers]

#     # # Set the content type to include the charset
#     # content_type = resp.headers.get('Content-Type', 'application/json')
#     # if 'charset' not in content_type:
#     #     content_type += '; charset=utf-8'
#     # headers.append(('Content-Type', content_type))

#     # response = Response(resp.content, resp.status_code)
#     # return response
#     # headers = dict(request.headers)
#     # headers['Host'] = TELEGRAPH_URL.replace('https://', '')
#     # headers['Access-Control-Allow-Origin'] = headers.get('Access-Control-Allow-Origin') or "*"
#     # # headers['Access-Control-Allow-Origin'] = "*"
#     # # headers['Access-Control-Allow-Credentials'] = True
#     # headers['Access-Control-Allow-Methods'] = "GET,OPTIONS,PATCH,DELETE,POST,PUT"
#     # headers['Access-Control-Allow-Headers'] = "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version"
    
    
#     # response = requests.request(
#     #     method=request.method,
#     #     url=url,
#     #     headers=headers,
#     #     data=request.get_data(),
#     #     cookies=request.cookies,
#     #     allow_redirects=False,
#     #     stream=False)

#     # # Filter out headers not to be forwarded
#     # excluded_headers = ['content-length', 'transfer-encoding', 'connection']
#     # headers = [(name, value) for (name, value) in response.raw.headers.items()
#     #            if name.lower() not in excluded_headers]

#     # # Flatten header list to dictionary
#     # headers = {name: ", ".join(values) for name, values in headers}

#     # return Response(response.content, response.status_code, headers)
