import os

import sevenbridges as sbg

# Set env variable
api_endpoint = os.getenv("INPUT_API_ENDPOINT")
auth_token = os.getenv("INPUT_AUTH_TOKEN")
project_name = os.getenv("INPUT_PROJECT_NAME")
path = os.getenv("INPUT_PATH")

api = sbg.Api(url=api_endpoint, token=auth_token)
# Get project
project = [p for p in api.projects.query(limit=100).all() \
           if p.name == project_name]


def get_or_create_folder(api: sbg.Api, name: str, project_id: str = None,
                         parent_id: str = None):
    """Get and create folder"""
    query = api.files.query(project=project_id, names=[name],
                            parent=parent_id)
    if query:
        folder = query[0]
    else:
        folder = api.files.create_folder(
            name=folder_name, project=project_id, parent=parent_id
        )
    return folder


if os.path.isfile(path):
    api.files.upload(path=path, project=project[0].id)
else:
    upload_files = os.walk(path)
    # Create initial folder in project
    folder_name = os.path.basename(os.path.abspath(path))
    parent = get_or_create_folder(api=api, name=folder_name,
                                  project_id=project[0].id)
    # Map full folder path to its id
    folder_ids = {os.path.abspath(path): parent.id}
    for dirpath, dirnames, filenames in upload_files:
        folder_path = os.path.abspath(dirpath)
        # Create all directories on CAVATICA
        for dirs in dirnames:
            parent = get_or_create_folder(
                api=api, name=dirs, parent_id=folder_ids[folder_path]
            )
            full_folder_path = os.path.abspath(dirs)
            folder_ids[full_folder_path] = parent.id
        # upload all files
        for files in filenames:
            api.files.upload(path=files,
                             parent=folder_ids[folder_path],
                             overwrite=True)
