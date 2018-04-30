# -*- coding: UTF-8 -*- #

import sys
import token_manager
import parser


def main(already_tried=False):
    if not already_tried:
        token = token_manager.get_access_token()
    else:
        token = token_manager.reset_access_token()
    response = parser.parse_command(sys.argv, token)
    if response is None:
        # comando erroneo (error del usuario)
        pass
    elif response.status_code != 200:
        # problema al ejecutar el comando (error de la aplicación)
        print '\033[31mNo se ha podido completar la operación\033[0m'
        if not already_tried:
            _manage_error(response)
    else:
        print 'Hecho!'


def _manage_error(response):
    code = response.status_code
    if code == 400:
        # Bad input parameter.
        _manage400()
    elif code == 401:
        # Bad or expired token.
        _manage401()
    elif code/100 == 5:
        # An error occurred on the Dropbox servers.
        _manage5xx()
    else:
        # Alguna otra cosa
        print code
        print response.content


def _manage400():
    main(True)


def _manage401():
    main(True)


def _manage5xx():
    print '\033[33mNo se puede acceder a Dropbox en estos momentos\033[0m'


if __name__ == '__main__':
    main()
