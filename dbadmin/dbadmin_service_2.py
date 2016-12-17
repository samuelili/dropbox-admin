import dropbox
from dropbox.files import DeleteError

'''
Recursively list all files under a folder including folders
:param folder:
:return:
'''


def list_folders(self, folder):
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


def list_folders_recursive(self, folder):
    files = []  # full of dictionaries
    for f in self.dbx.files_list_folder(folder).entries:
        f_dict = dict(name=f.name, path=f.path_lower, type='folder')
        if isinstance(f, dropbox.files.FolderMetadata):
            f_dict['children'] = self.list_folders(f_dict['path'])
            files.append(f_dict)

    return files


'''
    list out all files, including folders, in a directory.
    will not recursivly go through sub-folders
'''


def list_all(self):
    files = []
    for f in self.dbx.files_list_folder('').entries:  # retrieving names
        f_dict = dict(name=f.name, path=f.path_lower, type='file')
        if isinstance(f, dropbox.files.FolderMetadata):
            f_dict['type'] = 'folder'

        files.append(f_dict)

    return files  # return the array


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


def test(self):
    return self.dbxt.team_alpha_groups_list()


def write(self, filename, data):
    return self.dbx.files_upload(data, '/' + filename)

