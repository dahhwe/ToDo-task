# Проект TechTask

## Описание
Простоe ToDo-приложение для управления задачами.

## Предварительные требования
- [Docker](https://docs.docker.com/get-docker/)
- Docker Compose

## Установка

1. **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/dahhwe/TechTask.git
    cd TechTask
    ```

2. **Убедитесь, что Docker Desktop запущен.**

3. **Соберите и запустите приложение:**
    ```bash
    docker-compose up --build
    ```

4. **Доступ к приложению:**
    Откройте браузер и перейдите по адресу `http://localhost:8000`.


## Инициализация базы данных

1. **Создайте базу данных и таблицы:**
    ```bash
    docker exec -it <db_container_id> psql -U postgres -f /path/to/init_db.sql
    ```

Замените `<db_container_id>` на фактический ID контейнера базы данных.