# -*- coding: UTF-8 -*- #

from file_manager import FileManager


def parse_command(argv, token):
    file_manager = FileManager(token)
    command = argv[1].lower()
    upload_commands = ['subir', 'upload', 'up']
    download_commands = ['bajar', 'descargar', 'download', 'down']
    share_commands = ['compartir', 'enviar', 'mandar', 'share']
    delete_commands = ['borrar', 'eliminar', 'delete']
    response = None
    if command in upload_commands:
        response = _parse_upload(argv, file_manager)
    elif command in download_commands:
        response = _parse_download(argv, file_manager)
    elif command in share_commands:
        response = _parse_share(argv, file_manager)
    elif command in delete_commands:
        response = _parse_delete(argv, file_manager)
    else:
        print 'Comando {} desconocido'.format(command)
    return response


def _parse_upload(argv, file_manager):
    response = None
    try:
        path_to_upload = argv[2]
        upload_path = argv[3]
        print 'Subiendo el archivo {} a {} en Dropbox...'.format(path_to_upload, upload_path)
        response = file_manager.upload_file(path_to_upload, upload_path)
    except IndexError:
        print '\033[33mEsperados dos argumentos\033[0m'
    return response


def _parse_download(argv, file_manager):
    response = None
    try:
        path_to_download = argv[2]
        save_path = argv[3]
        print 'Descargando el archivo {} de Dropbox en {}...'.format(path_to_download, save_path)
        response = file_manager.download_file(path_to_download, save_path)
    except IndexError:
        print '\033[33mEsperados dos argumentos\033[0m'
    return response


def _parse_share(argv, file_manager):
    response = None
    try:
        path_to_share = argv[2]
        member = argv[3]
        message = ''
        if len(argv) >= 5:
            message = argv[4]
        print 'Compartiendo el archivo {} con {}...'.format(path_to_share, member)
        response = file_manager.share_file(path_to_share, member, message)
    except IndexError:
        print '\033[33mEsperados dos argumentos, y un tercero opcional\033[0m'
    return response


def _parse_delete(argv, file_manager):
    response = None
    try:
        path_to_delete = argv[2]
        response = file_manager.delete_file(path_to_delete)
        print 'Eliminando el archivo {}...'.format(path_to_delete)
    except IndexError:
        print '\033[33mEsperados un argumento\033[0m'
    return response
