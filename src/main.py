# -*- coding: UTF-8 -*- #

import sys
import token_manager
import parser
import json


def main(already_tried=False):
    if not already_tried:
        token = token_manager.get_access_token()
    else:
        # ha habido un error. El token guardado no es válido
        token = token_manager.reset_access_token()

    if token is not None:
        response = parser.parse_command(sys.argv, token)
        if response is None:
            # comando erroneo (error del usuario)
            pass
        elif response.status_code != 200:
            # problema al ejecutar el comando (error de la aplicación)
            if not already_tried:
                _manage_error(response)
            else:
                print '\033[31mNo se ha podido completar la operación\033[0m'
        else:
            print 'Hecho!'
    else:
        print '\033[31mNo se han obtenido permisos para realizar esa acción\033[0m'


def _manage_error(response):
    code = response.status_code
    if code == 400:
        # Bad input parameter.
        _manage400()
    elif code == 401:
        # Bad or expired token.
        _manage401()
    elif code == 409:
        # Endpoint-specific error.
        _manage409(response)
    elif code/100 == 5:
        # An error occurred on the Dropbox servers.
        _manage5xx()
    else:
        # Alguna otra cosa
        print '\033[33mOoops, ha surgido alguno de los errores para los que no he puesto tratamiento especializado.\033[0m'
        print '\033[33mAquí están el código de error y el mensaje devuelto por Dropbox.\033[0m'
        print code
        print response.content


def _manage400():
    main(True)


def _manage401():
    main(True)


def _manage409(response):
    response_json = json.loads(response.content)
    try:
        print '\033[33m{}\033[0m'.format(response_json['user_message']['text']).encode('utf-8')
    except KeyError:
        print '\033[33mAlgo ha ido mal en la petición. Revise que todos los parámetros son correctos\033[0m'


def _manage5xx():
    print '\033[33mNo se puede acceder a Dropbox en estos momentos\033[0m'


if __name__ == '__main__':
    main()
