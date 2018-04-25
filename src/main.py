# -*- coding: UTF-8 -*- #

import sys
import token_manager
import parser


def main():
    token = token_manager.get_access_token()
    response = parser.parse_command(sys.argv, token)
    if response is not None and response.status_code != 200:
        print '\033[31mNo se ha podido completar la operación\033[0m'
        _manage_error(response)
    else:
        print 'Hecho!'


def _manage_error(response):
    code = response.status_code
    if code == 401:
        _manage401()
    elif code/100 == 5:
        _manage5xx()
    else:
        print response.content


def _manage401():
    token = token_manager.reset_access_token()
    response = parser.parse_command(sys.argv, token)
    if response is not None and response.status_code != 200:
        print '\033[31mNo se ha podido completar la operación\033[0m'
    else:
        print 'Hecho!'


def _manage5xx():
    print '\033[33mNo se puede acceder a Dropbox en estos momentos\033[0m'


if __name__ == '__main__':
    main()
