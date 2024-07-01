from flask import Flask, request, Response
import requests

app = Flask(__name__)

DOCKER_REGISTRY_URL = "https://registry-1.docker.io"  # Docker官方镜像仓库URL
DOCKER_AUTH_URL = "https://auth.docker.io/token"      # Docker身份验证服务器URL
DOCKER_SERVICE = "registry.docker.io"                 # Docker服务名称

def get_docker_token(scope):
    params = {
        'service': DOCKER_SERVICE,
        'scope': scope
    }
    response = requests.get(DOCKER_AUTH_URL, params=params)
    response.raise_for_status()
    return response.json()['token']

def proxy_request(path, scope):
    token = get_docker_token(scope)
    docker_url = f"{DOCKER_REGISTRY_URL}{path}"
    headers = {
        key: value for key, value in request.headers if key != 'Host'
    }
    headers['Authorization'] = f'Bearer {token}'
    response = requests.request(
        method=request.method,
        url=docker_url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in response.raw.headers.items() if name.lower() not in excluded_headers]
    return Response(response.content, response.status_code, headers)

@app.route('/', defaults={'path': ''}, methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    scope = "registry:catalog:*" if path == "" else f"repository:library/{path.split('/')[0]}:pull"
    return proxy_request(f"/v2/{path}", scope)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
