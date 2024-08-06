

Start Redis $ redis-server
Start Celery worker $ celery -A web.apis.tasks worker --loglevel=info --pool=solo
Start Flask Server 

