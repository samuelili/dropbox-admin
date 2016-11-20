import dropbox
import yaml

with open('../token.yaml', 'r') as f:
    config = yaml.load(f.read())

token = config['dropbox-token']
id = config['id']

dbxt = dropbox.DropboxTeam(token)
dbx = dbxt.as_user(id)

links = dbx.sharing_list_shared_links().links

# for link in links:
#     if link.name == 'Hello1':
#         print link
#         dbx.sharing_revoke_shared_link(link.url)

entries = dbx.files_list_folder('').entries

for entry in entries:
    if entry.name == 'Hello1':
        print entry
        dbx.sharing_create_shared_link_with_settings(entry.path_lower)
