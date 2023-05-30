# The Bewise-Quiz API
This app provides API to register users, upload and download wav files.

The app provides functionality as follows:
 - Register a new user
 - Upload a wav file with conversion to mp3 format
 - Download a mp3 file
 
---

**Technologies used in the project:**
 
 - Fast-API 
 - SQLAlchemy 
 - Uvicorn
 - Poetry
 - Pydantic
 - Docker
 - Docker-compose

---

**Project's structure:**
 
 - dao - data access objects to work with database
 - services - service objects with business logic
 - constants.py - constants to configure the application
 - uploads - uploaded music files
 - container.py - DAO and Service instances
 - Docker-compose.yaml - main file to start the application by using Docker
 - Dockerfile - description of the image to create API container
 - create_db.py - creation db tables
 - main.py - file with FastApi application to start
 - utils.py - utility functions
 - README.md - this file with project description
---

**How to start the project:**
The app is ready to install out of the box. There are two containers in the docker - db providing database and
api with the application.
To start the app just follow the next steps:
 - Clone the repository
 - Install docker and docker-compose packages by the command `sudo apt install docker.io docker-compose`
 - Prepare .env file using an example provided below
 - Prepare docker-compose.yaml file (change settings such as ports, images if you need)
 - Start the app by using `sudo docker-compose up -d` command
 - The main page with swagger will be available by the url http://localhost/ (if started locally) or http://yourdomain/ 
(if started on the server)
 - After that application is ready to process requests

---

**An example of request:**

- POST: http://localhost/users/register
- json: {"username": "legat777"}
- responses:
`
    {
      "id": 1,
      "uuid": '05646e346a1b47cb8fb20d3bd8a331b5'      
    } `

- POST: http://localhost/files/upload??user_id=10&uuid=05646e346a1b47cb8fb20d3bd8a331b5
- form-data: file
- responses:
`
    http://localhost:80/record?id=10&user=1

- GET: http://localhost:80/record?id=10&user=1
- responses:
    200 OK    

---
Example of .env file:

    POSTGRES_DB=booking - your db name
    POSTGRES_PASSWORD=plamer0805 - db username's password
    POSTGRES_USER=plamer - db username
    POSTGRES_PORT=5432 - db port
    POSTGRES_HOST=db - database host (the name of docker container)
    CLEAR_DB=True - if True then all tables will be deleted each time you start the application
    API_VERSION=1.0.0 - current API version (all three settings used only for swagger)
    API_TITLE=Bewise Quiz API - API title
    API_DESCRIPTION=This API allows you to save unique questions for quiz in database - API description
    SERVER_HOST=localhost - domain or ip address or your host (localhost if started locally or ip address(domain) or your server)
    SERVER_PORT=80 - port the application runs on (default is 80)


The project was created by Alexey Mavrin in 30 May 2023