create_content_schema:
	echo "Создать схему content в базе данных."
	docker-compose up -d --build postgres
	docker exec -d postgres psql -Upostgres -d postgres -c "CREATE SCHEMA IF NOT EXISTS content;"


start-admin:
	echo "Запуск проекта"
	docker-compose up -d --build backend_admin postgres nginx es redis etl
	docker-compose logs -f

# Remove all containers
kill_all_containers:
	docker-compose down -v --remove-orphans

