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
  upload_file:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: upload file
      uses: include-dcc/cavatica-upload-action@v0.0.3
      with:
        auth_token: ${{ secrets.AUTH_TOKEN }}
        project_name: Test
        path: README.md

  upload_dir:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: upload file
      uses: include-dcc/cavatica-upload-action@v0.0.3
      with:
        auth_token: ${{ secrets.AUTH_TOKEN }}
        project_name: Test
        folder_name: test_space
        path: "./"
```

* `folder_name` can be specified but it must be a-z, A-Z, 0-9, and special characters (_), (-), and (.). Names can't be longer than 255 characters. Spaces are not allowed.
