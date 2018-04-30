# -*- coding: UTF-8 -* #

import urllib
import webbrowser
import socket
import requests
import json
import os


def _obtain_auth_code():
    """Pide permiso al usuario y obtiene y devuelve el código de autorización obtenido.
    Devuelve None si el usuario no concede el permiso."""

    data_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/data.json'
    try:
        with open(data_path, 'r') as file:
            data_json = json.load(file)
        dropbox_app_key = data_json['dropbox_app_key']
    except (KeyError, ValueError, IOError):
        print 'Error en la configuración del proyecto'
        exit(1)

    server = 'www.dropbox.com'
    params = {'response_type': 'code',
              'client_id': dropbox_app_key,
              'redirect_uri': 'http://localhost:8080'}
    encoded_params = urllib.urlencode(params)
    resource = '/1/oauth2/authorize?' + encoded_params
    uri = 'https://' + server + resource
    webbrowser.open_new(uri)

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('localhost', 8080))
    listen_socket.listen(1)
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    http_response = """\
    HTTP/1.1 200 OK
    <html>
    <head><title>Prueba </title></head>
    <body>
    The authentication flow has completed. Close this window.
    </body>
    </html>"""
    client_connection.sendall(http_response)
    client_connection.close()

    param = request.split('\n')[0].split('?')[1]
    name = param.split('=')[0].split(' ')[0]
    if name == 'code':
        code = param.split('=')[1].split(' ')[0]
    else:
        code = None

    return code


def _obtain_access_token(auth_code):
    """Obtiene y devuelve el token de acceso concedido por el código de autenticación auth_code.
    Si no se puede obtener el token, devuelve None"""

    data_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/data.json'
    try:
        with open(data_path, 'r') as file:
            data_json = json.load(file)
        dropbox_app_key = data_json['dropbox_app_key']
        dropbox_secret_key = data_json['dropbox_secret_key']
    except (KeyError, ValueError, IOError):
        print 'Error en la configuración del proyecto'
        exit(1)

    headers = {'User_Agent': 'Python_Client',
               'Content_Type': 'application/x-www-form-urlenconded'}
    data = {'code': auth_code,
            'grant_type': 'authorization_code',
            'client_id': dropbox_app_key,
            'client_secret': dropbox_secret_key,
            'redirect_uri': 'http://localhost:8080'}

    response = requests.post('https://api.dropboxapi.com/1/oauth2/token',
                             headers=headers,
                             data=data)
    response_json = json.loads(response.content)

    try:
        return response_json['access_token']
    except KeyError:
        return None


def _read_access_token():
    """Lee y devuelve el token de acceso. Devuelve None si no se puede leer el token."""

    path = os.path.dirname(os.path.abspath(__file__)) + '/resources/access_token.json'
    if os.path.isfile(path):
        try:
            with open(path, 'r') as file:
                code_json = json.load(file)
            key = 'access_token'
            if key in code_json:
                return code_json[key]
        except (KeyError, ValueError, IOError):
            return None


def _save_access_token(token):
    """Guarda el token de acceso en formato json"""

    path = os.path.dirname(os.path.abspath(__file__)) + '/resources/access_token.json'
    code = {'access_token': token}
    with open(path, 'w') as file:
        json.dump(code, file)


def reset_access_token():
    """Intenta obtener el token de acceso a partir de la autorización del usuario.
    Devuelve None si no se obtiene el permiso del usuario."""

    auth_code = _obtain_auth_code()
    if auth_code is not None:
        access_token = _obtain_access_token(auth_code)
        if access_token is not None:
            _save_access_token(access_token)
        return access_token


def get_access_token():
    """Intenta obtener el token de acceso leyéndolo desde el archivo en el que se guarda.
    Si no lo consigue, intenta obtener uno nuevo a partir de la autorizacion del usuario"""

    # se intenta leer el access_token guardado
    access_token = _read_access_token()
    if access_token is None:
        # si no se puede, se intenta obtener uno nuevo
        access_token = reset_access_token()
    return access_token


if __name__ == '__main__':
    pass
