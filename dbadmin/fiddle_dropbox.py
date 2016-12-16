from dropbox import dropbox

import dbadmin_service

with open('token.txt', 'r')as f:
    global token
    token = f.read()

dbx = dropbox.Dropbox(token)

service = dbadmin_service.DropboxService(token)

print(service.list_all_shared_folders())
