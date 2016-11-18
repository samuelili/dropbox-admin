import json
import os
from datetime import datetime

import dropbox
import jsonpickle
import operator
from dropbox.files import DeleteError

PATH_SHARED_FOLDER_LIST_RESULT = "/tmp/dropbox_list_result.json"


class DropboxService:
    def __init__(self, token=None):
        self.members = None
        self.dbx = dropbox.Dropbox(token)
        self.dbxt = dropbox.DropboxTeam(token)
        self.progress = {"processed": 0, "total": 1}

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

    def list_all_shared_folders(self, force_update=True):
        if self.__should_update() or force_update:
            self.members = []
            dbx_members = self.dbxt.team_members_list().members
            for dbx_member in dbx_members:
                self.members.append({
                    "team_id": dbx_member.profile.team_member_id,
                    "name": dbx_member.profile.name.display_name,
                    "shared": []
                })

            self.progress["processed"] = 0
            self.progress["total"] = len(self.members)

            for member in self.members:
                print member["name"]
                dbx = self.dbxt.as_user(member["team_id"])
                for entry in dbx.sharing_list_folders().entries:
                    member["shared"].append({
                        "name": entry.name,
                        "path": entry.path_lower,
                        "time_invited": entry.time_invited.strftime("%x"),
                        "days_old": (datetime.now() - entry.time_invited).days,
                        "preview_url": entry.preview_url,
                        "access_type": self.__get_access_type(entry.access_type),
                        "shared_folder_id": entry.shared_folder_id
                    })
                self.progress["processed"] += 1

            self.members.sort(key=operator.itemgetter('name'))

            with open(PATH_SHARED_FOLDER_LIST_RESULT, "wb") as output_file:
                json.dump(json.loads(jsonpickle.encode(self.members)), output_file)
        else:
            with open(PATH_SHARED_FOLDER_LIST_RESULT, "r") as f:
                self.members = json.load(f)

        return self.members

    @staticmethod
    def __get_access_type(dbx_access):
        if dbx_access.is_owner():
            return "owner"
        elif dbx_access.is_editor():
            return "editor"
        elif dbx_access.is_viewer():
            return "viewer"
        else:
            return "other"

    @staticmethod
    def __should_update():
        if not os.path.exists(PATH_SHARED_FOLDER_LIST_RESULT):
            return True
        delta = datetime.now() - datetime.fromtimestamp(os.stat(PATH_SHARED_FOLDER_LIST_RESULT).st_mtime)
        return delta.seconds > 24 * 60 * 60

    def write(self, filename, data):
        return self.dbx.files_upload(data, '/' + filename)

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
