# -*- coding: UTF-8 -*- #
import requests
import urllib
import webbrowser
import socket
import json

######################################################################################
#  CREDENCIALES de la Aplicación
######################################################################################
dropbox_app_key = '71zvorjzg9ypleh'
dropbox_app_secret = 'ts7avyhdp11p5po'
######################################################################################
#  CODE: Abrir en el navegador la URI
#  https://www.dropbox.com//oauth2/authorize
######################################################################################
servidor = 'www.dropbox.com'
params = {'response_type': 'code', 'client_id': dropbox_app_key, 'redirect_uri': 'http://localhost:8080'}
params_encoded = urllib.urlencode(params)
recurso = '/1/oauth2/authorize?' + params_encoded
uri = 'https://' + servidor + recurso
webbrowser.open_new(uri)
print '###############################################################################'
print '---- Petición al usuario de Autenticación y Permiso: Devuelve el Code'
print '-------------------------------------------------------------------------------'
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('localhost', 8080))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % 8080
client_connection, client_address = listen_socket.accept()
request = client_connection.recv(1024)
print "Conexion local Respuesta:"
print request
http_response = """\ HTTP/1.1 200 OK The authentication flow has completed. Close this window. """
client_connection.sendall(http_response)
client_connection.close()
code = request.split('\n')[0].split('?')[1].split('=')[1].split(' ')[0]
print "code: "+ code
######################################################################################
#  ACCESS_TOKEN: Obtener el TOKEN
#  https://www.api.dropboxapi.com/1/oauth2/token
#####################################################################################
print '###############################################################################'
print '---- Obtención del Access_Token'
print '-------------------------------------------------------------------------------'
parametros = {'code': code, 'grant_type': 'authorization_code', 'client_id': dropbox_app_key, 'client_secret': dropbox_app_secret, 'redirect_uri': 'http://localhost:8080' }
cabeceras={'User-Agent':'Python Client'}
respuesta = requests.post('https://api.dropboxapi.com/1/oauth2/token', headers=cabeceras, data=parametros)
print respuesta.status_code
json_respuesta = json.loads(respuesta.content)
print json_respuesta
access_token = json_respuesta['access_token']
print "Access_Token: " + access_token
######################################################################################
#  DROPBOX Api : Lista el contenido de un diectorio
#  https://api.dropboxapi.com/2/files/list_folder
######################################################################################
print '###############################################################################'
print '---- Listar el contenido de un directorio'
print '-------------------------------------------------------------------------------'
path="/SAD"
cuerpo = {"path": path, "recursive": True, "include_has_explicit_shared_members": False}
cuerpo = json.dumps(cuerpo)
cabeceras = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
# REALIZAMOS LA PETICION
respuesta = requests.post('https://api.dropboxapi.com/2/files/list_folder', headers=cabeceras, data=cuerpo)
# PROCESAMOS LA RESPUESTA
print respuesta.status_code
cuerpo = respuesta.content
if respuesta.status_code!=200:
    cuerpo = json.loads(cuerpo)
    print 'Error: '+ cuerpo["error_summary"]
else:
    cuerpo= json.loads(cuerpo)
    print "\nLista de Ficheros:"
    for each in cuerpo["entries"]:
        print ' ' + each['name'] + '--' + each['.tag']
