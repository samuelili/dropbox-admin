from dropbox import files, dropbox

import dropbox_service

with open('token.txt', 'r')as f:
    global token
    token = f.read()

dbx = dropbox.Dropbox(token)

service = dropbox_service.DropboxService(token)

print(service.list_all_shared_folders())
