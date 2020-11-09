build:
	docker-compose up -d --build
	docker exec -it breakingbadapi_task_django_1 bash

container:
	docker exec -it breakingbadapi_task_django_1 bash

test:
	DJANGO_SETTINGS_MODULE=breakingbadapi_task.settings.test pytest $(TEST_ME_PLEASE)

shell:
	django-admin shell_plus
