# django-celery-stability-ai
a simple django drf api with celery worker to generate text to image using stability ai

## Requirements
-  python3
- docker(for redis) or Redis at localhost:6379

## setup
- create a virtual env
- source ./env/bin/active
- cd api/
- pip install -r requirements.txt

## starting server and celery
- In one terminal
    - cd api/
    - python manage.py runserver
- In another terminal(redis)
    - docker run --name my-redis -p 6379:6379 -d redis
- In another terminal
    - cd api/
    - celery -A api worker --loglevel=info --concurrency 5

## or use docker
- cd api/
- sudo docker-compose up --build


## Routes
- /login POST
    Request Body:   {"username":"username","password":"password"}
    Response (200): {"status":"success","username": "test","tokens":{"refresh_token":"token","access_token":"token"}}
- /register POST
    Request Body : {"email":email,"username:"unique_username","password":"password"}
    Response(200):{
        "status":"success",
        "tokens":{"refresh_token":"token","access_token":"token"}
    }

 Protected Routes
 in header:
    Authorization: Bearer <token>
- /health GET
    response {"status":"working"}
- /task POST
    Request body: {"text":"text to image prompt"}
    response: {"status":"success"}
- /all-tasks GET
    Response(all request list):[{
        "id":id,
        "request_time:time,
        "text":prompt,
        "status":success/error/pending/none/working,
        "error":if any
        "image_url":"url of image generated"
    }]
