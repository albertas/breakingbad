build:
	docker-compose up -d --build
	docker exec -it breakingbadapi_task_django_1 bash

container:
	docker exec -it breakingbadapi_task_django_1 bash
