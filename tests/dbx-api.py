import json
from datetime import datetime

import dropbox
import jsonpickle

dbxt = dropbox.DropboxTeam("enter token here")

dbx_members = dbxt.team_members_list().members

members = []

for dbx_member in dbx_members:
    members.append({
        "team_id": dbx_member.profile.team_member_id,
        "name": dbx_member.profile.name.display_name,
        "shared": []
    })


def get_access_type(dbx_access):
    if dbx_access.is_owner():
        return "owner"
    elif dbx_access.is_editor():
        return "editor"
    elif dbx_access.is_viewer():
        return "viewer"
    else:
        return "other"


for member in members:
    dbx = dbxt.as_user(member["team_id"])
    for entry in dbx.sharing_list_folders().entries:
        member["shared"].append({
            "name": entry.name,
            "path": entry.path_lower,
            "time_invited": entry.time_invited.strftime("%x"),
            "days_old": (datetime.now() - entry.time_invited).days,
            "preview_url": entry.preview_url,
            "access_type": get_access_type(entry.access_type),
            "shared_folder_id": entry.shared_folder_id
        });
    print json.dumps(json.loads(jsonpickle.encode(member)), indent=4)
    print "++++++++++++++++++++++++++++++++++++++++++++"



# print json.dumps(json.loads(jsonpickle.encode(members)), indent=4)


#
#
# for entry in dbx.sharing_list_folders().entries:
#     print(entry)
#
# print json.dumps(json.loads(jsonpickle.encode(members)), indent=2)
#
