import json
import os
from datetime import datetime

import dropbox
import jsonpickle
import operator

PATH_SHARED_FOLDERS_LIST_RESULT = "/tmp/dropbox_list_shared_folders_result.json"
PATH_SHARED_LINKS_RESULT = "/tmp/dropbox_list_shared_links_result.json"


class DropboxService:
    def __init__(self, token=None):
        self.dbxt = dropbox.DropboxTeam(token)
        self.progress = {"processed": 0, "total": 1}

    def list_all_shared_links(self, force_update=True):
        """
        List all shared links of all team members
        :param force_update:
        :return:
        """
        if self.__should_update(PATH_SHARED_LINKS_RESULT) or force_update:
            members = self.list_team_members()
            self.progress["total"] = len(members)
            self.progress["processed"] = 0

            for member in members:
                member["links"] = self.list_shared_links(member["team_member_id"])
                self.progress["processed"] += 1
                print self.progress

            members.sort(key=operator.itemgetter('display_name'))

            with open(PATH_SHARED_LINKS_RESULT, "wb") as output_file:
                json.dump(json.loads(jsonpickle.encode(members)), output_file)
        else:
            with open(PATH_SHARED_LINKS_RESULT, "r") as f:
                members = json.load(f)

        return members

    def list_all_shared_folders(self, force_update=True):
        """
        List all shared folders of all team members
        :param force_update:
        :return:
        """
        if self.__should_update(PATH_SHARED_FOLDERS_LIST_RESULT) or force_update:
            members = self.list_team_members()
            self.progress["total"] = len(members)
            self.progress["processed"] = 0

            for member in members:
                member["shared"] = self.list_shared_folders(member["team_member_id"])
                self.progress["processed"] += 1
                print self.progress

            with open(PATH_SHARED_FOLDERS_LIST_RESULT, "wb") as output_file:
                json.dump(json.loads(jsonpickle.encode(members)), output_file)
        else:
            with open(PATH_SHARED_FOLDERS_LIST_RESULT, "r") as f:
                members = json.load(f)

        return members

    def list_team_members(self):
        """
        List all team members.
        :return:
        """
        members = []
        dbx_members = self.dbxt.team_members_list().members
        for dbx_member in dbx_members:
            members.append({
                "team_member_id": dbx_member.profile.team_member_id,
                "account_id": dbx_member.profile.account_id,
                "display_name": dbx_member.profile.name.display_name
            })

        members.sort(key=operator.itemgetter('display_name'))
        return members

    def list_shared_links(self, team_member_id):
        """
        List all shared links of a team member.
        :param team_member_id:
        :return:
        """
        dbx = self.dbxt.as_user(team_member_id)
        result = dbx.sharing_list_shared_links()
        links = []
        for link in result.links:
            links.append({
                "id": link.id,
                "name": link.name,
                "path": link.path_lower,
                "url": link.url,
                "can_revoke": link.link_permissions.can_revoke,
                "visibility": self.__get_link_visibility(link.link_permissions.resolved_visibility),
                "expires": link.expires
            })
        return links

    def list_shared_folders(self, team_member_id):
        """
        Lists the shared folders of a team member.

        :param team_member_id:
        :return:
        """
        dbx = self.dbxt.as_user(team_member_id)
        shared_folders = []
        for entry in dbx.sharing_list_folders().entries:
            shared_folders.append({
                "name": entry.name,
                "path": entry.path_lower,
                "time_invited": entry.time_invited.strftime("%x"),
                "days_old": (datetime.now() - entry.time_invited).days,
                "preview_url": entry.preview_url,
                "access_type": self.__get_access_type(entry.access_type),
                "shared_folder_id": entry.shared_folder_id
            })

        return shared_folders

    def get_member_info(self, team_member_id, account_id):
        dbx = self.dbxt.as_user(team_member_id)
        account = dbx.users_get_account(account_id)
        return {
            "name": account.name,
            "account_id": account.account_id,
            "team_member_id": account.team_member_id,
            "email": account.email
        }

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
    def __should_update(check_file):
        if not os.path.exists(check_file):
            return True
        delta = datetime.now() - datetime.fromtimestamp(os.stat(check_file).st_mtime)
        return delta.seconds > 24 * 60 * 60

    @staticmethod
    def __get_link_visibility(visibility):
        if visibility.is_shared_folder_only():
            return "Shared Folder"
        elif visibility.is_team_and_password:
            return "Team and Password"
        else:
            return "Others"

