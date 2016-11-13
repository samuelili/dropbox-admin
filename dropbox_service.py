import datetime

import dropbox
from dropbox.files import DeleteError


class DropboxService:
    def __init__(self, token=None):
        self.dbx = dropbox.Dropbox(token)

    '''
    Recursively list all files under a folder including folders
    :param folder:
    :return:
    '''
    def list(self, folder):
        files = []  # full of dictionaries
        for f in self.dbx.files_list_folder(folder).entries:
            f_dict = dict(name=f.name, path=f.path_lower, type='file')
            if isinstance(f, dropbox.files.FolderMetadata):
                f_dict['file'] = 'folder'
                f_dict['children'] = self.list(f_dict['path'])
            files.append(f_dict)

        return files

    '''
    Recursively list all sub-folders of a folder.
    :param folder:
    :return:
    '''

    def list_folders(self, folder):
        files = []  # full of dictionaries
        for f in self.dbx.files_list_folder(folder).entries:
            f_dict = dict(name=f.name, path=f.path_lower, type='folder')
            if isinstance(f, dropbox.files.FolderMetadata):
                f_dict['children'] = self.list_folders(f_dict['path'])
                files.append(f_dict)

        return files

    '''
    List all shared folders.
    '''
    def list_all_shared_folders(self):
        files = []  # full of dictionaries
        for f in self.dbx.files_list_folder('').entries:
            f_dict = dict(name=f.name, path=f.path_lower, type='folder')
            if isinstance(f, dropbox.files.FolderMetadata) & (f.sharing_info is not None):
                f_dict['children'] = self.list_folders(f_dict['path'])
                files.append(f_dict)

        return files

    def write(self, filename, data):
        return self.dbx.files_upload(data, '/' + filename)

    def read(self):
        entries = []
        epoch = datetime.datetime.utcfromtimestamp(0)
        for entry in self.dbx.files_list_folder('').entries:  # retrieving names
            entrydict = {
                'modified': (entry.client_modified - epoch).total_seconds() * 1000,
                'name': entry.name,
                'size': entry.size
            }

            entries.append(entrydict)
        return entries  # return the array

    def delete(self, filename):
        try:
            self.dbx.files_delete('/' + filename)  # delete
            return 200
        except DeleteError:
            return 404

    '''
        for debugging purposes.
        :returns dropbox instance
    '''
    def get_dropbox(self):
        return self.dbx
