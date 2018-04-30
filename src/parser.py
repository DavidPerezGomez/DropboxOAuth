# -*- coding: UTF-8 -*- #

from file_manager import FileManager


def parse_command(argv, token):
    file_manager = FileManager(token)
    command = argv[1].lower()
    upload_commands = ['subir', 'upload', 'up']
    download_commands = ['bajar', 'descargar', 'download', 'down']
    share_commands = ['compartir', 'enviar', 'mandar', 'share']
    delete_commands = ['borrar', 'eliminar', 'delete', 'rm']
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
        local_path_to_upload = argv[2]
        remote_save_path = argv[3]
        print 'Subiendo el archivo {} a {} en Dropbox...'.format(local_path_to_upload, remote_save_path)
        response = file_manager.upload_file(local_path_to_upload, remote_save_path)
    except IndexError:
        print '\033[33mEsperados dos argumentos\033[0m'
        print 'Ejemplo: upload /mi/archivo/local /ruta/dropbox/donde/guardar'
    return response


def _parse_download(argv, file_manager):
    response = None
    try:
        remote_path_to_download = argv[2]
        local_save_path = argv[3]
        print 'Descargando el archivo {} de Dropbox en {}...'.format(remote_path_to_download, local_save_path)
        response = file_manager.download_file(remote_path_to_download, local_save_path)
    except IndexError:
        print '\033[33mEsperados dos argumentos\033[0m'
        print 'Ejemplo: download /mi/archivo/dropbox /ruta/local/donde/guardar'
    return response


def _parse_share(argv, file_manager):
    response = None
    try:
        remote_path_to_share = argv[2]
        member = argv[3]
        message = ''
        if len(argv) >= 5:
            message = argv[4]
        print 'Compartiendo el archivo {} con {}...'.format(remote_path_to_share, member)
        response = file_manager.share_file(remote_path_to_share, member, message)
    except IndexError:
        print '\033[33mEsperados dos argumentos, y un tercero opcional\033[0m'
        print 'Ejemplo: share /mi/archivo/dropbox usuario@destino.com \"mensaje opcional\"'
    return response


def _parse_delete(argv, file_manager):
    response = None
    try:
        remote_path_to_delete = argv[2]
        response = file_manager.delete_file(remote_path_to_delete)
        print 'Eliminando el archivo {}...'.format(remote_path_to_delete)
    except IndexError:
        print '\033[33mEsperados un argumento\033[0m'
        print 'Ejemplo: delete /mi/archivo/dropbox'
    return response
