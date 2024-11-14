build:
	sudo docker compose build web && npm install

build-no-cache:
	sudo docker compose build web --no-cache

restart:
	docker compose down --remove-orphans && docker compose up -d

start:
	docker compose up -d

down:
	docker compose down --remove-orphans

remove_db:
	sudo rm -rf ./dev/data/db

change_db_owner:
	sudo chown $(USER):$(USER) data/db -R

compile_packages:
	docker compose up -d && \
	docker exec dev-event_tool pip install pip-tools && \
	docker exec --workdir /requirements dev-event_tool pip-compile && \
	docker compose down --remove-orphans && \
	docker compose up -d

create_initial_data:
	docker exec -it dev-event_tool python manage.py create_initial_data

pre_commit_all_files:
	pre-commit run --all-files
