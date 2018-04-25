# "-*- coding: UTF-8 -*- #

import requests
import os
import json


class FileManager:

    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, path_to_upload, upload_path):
        while upload_path.startswith('/'):
            upload_path = upload_path[1:]
        upload_path = '/' + upload_path

        uri = 'https://content.dropboxapi.com/2/files/upload'
        dropbox_api_arg = {'path': upload_path,
                           'mode': 'add',
                           'autorename': True,
                           'mute': False}
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Dropbox-API-Arg': json.dumps(dropbox_api_arg),
                   'Content-Type': 'application/octet-stream'}
        with open(os.path.expanduser(path_to_upload), 'rb') as file:
            data = file.read()

        response = requests.post(uri, headers=headers, data=data)

        if response.status_code != 200:
            pass
        return response

    def download_file(self, path_to_download, save_path):
        while path_to_download.startswith('/'):
            path_to_download = path_to_download[1:]
        path_to_download = '/' + path_to_download

        uri = 'https://content.dropboxapi.com/2/files/download'
        dropbox_api_arg = {'path': path_to_download}
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Dropbox-API-Arg': json.dumps(dropbox_api_arg)}

        response = requests.post(uri, headers=headers)

        if response.status_code == 200:
            file_content = response.content
            with open(os.path.expanduser(save_path), 'wb') as file:
                file.write(file_content)
        else:
            pass
        return response

    def delete_file(self, path_to_delete):
        while path_to_delete.startswith('/'):
            path_to_delete = path_to_delete[1:]
        path_to_delete = '/' + path_to_delete

        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Content-Type': 'application/json'}
        data = {'path': path_to_delete}
        data = json.dumps(data)

        response = requests.post(uri, headers=headers, data=data)

        if response.status_code != 200:
            pass
        return response

    def share_file(self, path_to_share, member_email, message=''):
        while path_to_share.startswith('/'):
            path_to_share = path_to_share[1:]
        path_to_share = '/' + path_to_share

        uri = 'https://api.dropboxapi.com/2/sharing/add_file_member'
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Content-Type': 'application/json'}
        data = {'file': path_to_share,
                'members': [{'.tag': 'email', 'email': member_email}],
                'custom_message': message,
                'quiet': False,
                'access_level': 'viewer'}
        data = json.dumps(data)

        response = requests.post(uri, headers=headers, data=data)

        if response.status_code != 200:
            pass
        return response
