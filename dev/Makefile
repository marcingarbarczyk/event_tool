build:
	sudo docker compose build web

build-no-cache:
	sudo docker compose build web --no-cache

restart:
	docker compose restart

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

remove_db_volume:
	sudo rm -rf ./data/db

remove_redis_volume:
	sudo rm -rf ./data/redis

remove_all_volumes:
	$(MAKE) remove_db_volume
	$(MAKE) remove_redis_volume

change_db_owner:
	sudo chown $(USER):$(USER) data/db -R

compile_packages:
	docker compose up -d && \
	docker exec dev-event_tool pip install pip-tools && \
	docker exec --workdir /requirements dev-event_tool pip-compile && \
	docker compose down --remove-orphans && \
	docker compose up -d

staging-up:
	cd ../staging/event_tool_staging/ && docker compose up -d

staging-down:
	cd ../staging/event_tool_staging/ && docker compose down --remove-orphans