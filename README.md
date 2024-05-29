git pull


frontend:
    cd frontend; npm start

backend:
    cd apps
    chmod 777 ./run_celery.sh
    python3 app.py
    ./run_celery.sh



