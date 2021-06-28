## About

Github Action to upload files to [CAVATICA](https://cavatica.sbgenomics.com/).


## Usage
To upload files to CAVATICA, authentication tokens and preexisting CAVATICA projects are required.

```
name: ci

on:
  push:
    branches: master

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
    - name: upload file
      uses: include-dcc/cavatica-upload-action@0.1
      with:
        auth_token: ${{ secrets.AUTH_TOKEN }}
        project_name: Test
        file_path: README.md
```
