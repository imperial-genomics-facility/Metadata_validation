# Metadata_validation
A flask based metadata validation server

## Docker image

Use the following docker image to run this server

  [avikdatta/metadata_validation_docker](https://hub.docker.com/r/avikdatta/metadata_validation_docker/)
  
  ```
  <p>docker pull avikdatta/metadata_validation_docker</p>
  ```

### Required env variables

Set the following environment variables before running the flask app

* FLASK_INSTANCE_PATH
  <p>A directory path for creating temporary files</p>

* FLASK_SECRET_KEY
  <p>A secret key for flask server</p>

* FLASK_CSRF_SECRET_KEY
  <p>A secret CSRF key for flask server</p>

* SAMPLESHEET_SCHEMA
  <p>A validation json schema for samplesheet file</p>

* METADATA_SCHEMA
  <p>A validation json schema metadata files</p>
