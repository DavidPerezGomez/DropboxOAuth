# "-*- coding: UTF-8 -*- #

import requests
import os
import json


class FileManager:

    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, local_path_to_upload, remote_save_path):
        if os.path.isfile(local_path_to_upload):
            while remote_save_path.startswith('/'):
                remote_save_path = remote_save_path[1:]
            remote_save_path = '/' + remote_save_path

            uri = 'https://content.dropboxapi.com/2/files/upload'
            dropbox_api_arg = {'path': remote_save_path,
                               'mode': 'add',
                               'autorename': True,
                               'mute': False}
            headers = {'Authorization': 'Bearer ' + self.access_token,
                       'Dropbox-API-Arg': json.dumps(dropbox_api_arg),
                       'Content-Type': 'application/octet-stream'}
            with open(os.path.expanduser(local_path_to_upload), 'rb') as file:
                data = file.read()

            response = requests.post(uri, headers=headers, data=data)

            return response

    def download_file(self, remote_path_to_download, local_save_path):
        while remote_path_to_download.startswith('/'):
            remote_path_to_download = remote_path_to_download[1:]
        remote_path_to_download = '/' + remote_path_to_download

        uri = 'https://content.dropboxapi.com/2/files/download'
        dropbox_api_arg = {'path': remote_path_to_download}
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Dropbox-API-Arg': json.dumps(dropbox_api_arg)}

        response = requests.post(uri, headers=headers)

        if response.status_code == 200:
            file_content = response.content
            with open(os.path.expanduser(local_save_path), 'wb') as file:
                file.write(file_content)

        return response

    def delete_file(self, remote_path_to_delete):
        while remote_path_to_delete.startswith('/'):
            remote_path_to_delete = remote_path_to_delete[1:]
        remote_path_to_delete = '/' + remote_path_to_delete

        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Content-Type': 'application/json'}
        data = {'path': remote_path_to_delete}
        data = json.dumps(data)

        response = requests.post(uri, headers=headers, data=data)

        return response

    def share_file(self, remote_path_to_share, member_email, message=''):
        while remote_path_to_share.startswith('/'):
            remote_path_to_share = remote_path_to_share[1:]
        remote_path_to_share = '/' + remote_path_to_share

        uri = 'https://api.dropboxapi.com/2/sharing/add_file_member'
        headers = {'Authorization': 'Bearer ' + self.access_token,
                   'Content-Type': 'application/json'}
        data = {'file': remote_path_to_share,
                'members': [{'.tag': 'email', 'email': member_email}],
                'custom_message': message,
                'quiet': False,
                'access_level': 'viewer'}
        data = json.dumps(data)

        response = requests.post(uri, headers=headers, data=data)

        return response


if __name__ == '__main__':
    pass