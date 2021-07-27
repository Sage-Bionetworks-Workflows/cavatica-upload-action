import os

import sevenbridges as sbg

# Set env variable
api_endpoint = os.getenv("INPUT_API_ENDPOINT")
auth_token = os.getenv("INPUT_AUTH_TOKEN")
project_name = os.getenv("INPUT_PROJECT_NAME")
folder_name = os.getenv("INPUT_FOLDER_NAME")
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
            name=name, project=project_id, parent=parent_id
        )
    return folder

# TODO: Add folders / files to exclude
# If a file is added, store the file
if os.path.isfile(path):
    api.files.upload(path=path, project=project[0].id, overwrite=True)
else:
    # Set folder name to "workspace" if folder name not specified
    if folder_name is None:
        folder_name = os.path.basename(os.path.abspath(path))
    # Create initial folder in project
    initial_folder = get_or_create_folder(
        api=api, name=folder_name,
        project_id=project[0].id
    )
    # Map full folder path to its id
    folder_ids = {os.path.abspath(path): initial_folder.id}
    upload_files = os.walk(path)
    for dirpath, dirnames, filenames in upload_files:
        # Don't upload hidden folders
        folder_path = os.path.abspath(dirpath)
        # Create all directories on CAVATICA
        for dirs in dirnames:
            parent = get_or_create_folder(
                api=api, name=dirs, parent_id=folder_ids[folder_path]
            )
            full_folder_path = os.path.join(folder_path, dirs)
            folder_ids[full_folder_path] = parent.id
        # upload all files
        for files in filenames:
            api.files.upload(path=os.path.join(folder_path, files),
                             parent=folder_ids[folder_path],
                             overwrite=True)
