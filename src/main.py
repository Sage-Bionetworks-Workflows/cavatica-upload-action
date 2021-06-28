import os

import sevenbridges as sbg

# Set env variable
api_endpoint = os.getenv("INPUT_API_ENDPOINT")
auth_token = os.getenv("INPUT_AUTH_TOKEN")
project_name = os.getenv("INPUT_PROJECT_NAME")
file_path = os.getenv("INPUT_FILE_PATH")

api = sbg.Api(url=api_endpoint, token=auth_token)
# Get project
project = [p for p in api.projects.query(limit=100).all() \
           if p.name == project_name]

api.files.upload(path=file_path, project=project[0].id)
